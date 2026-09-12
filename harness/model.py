"""model.py - how we talk to the AI model.

This is the only file that touches the internet.

The model does not "do" anything. You send it a list of messages,
it sends back some text. Everything else in this harness is us
deciding what to send and what to do with the text that comes back.
"""

import json
import os
import time
import urllib.error
import urllib.request

# Where the harness looks for your settings. See .env.example.
ENV_FILE = ".env"


def load_env():
    """Read the .env file into a dictionary.

    A .env file is just lines of NAME=value. It is the normal way to keep
    a secret (like an API key) out of your code and out of the repository.
    """
    settings = {}
    if not os.path.exists(ENV_FILE):
        return settings
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            # Strip optional surrounding quotes, e.g. API_KEY="sk-123"
            settings[name.strip()] = value.strip().strip('"').strip("'")
    return settings


def settings():
    """The three things we need: a key, an address, and a model name."""
    env = load_env()
    return {
        "api_key": env.get("API_KEY", "").strip(),
        "base_url": env.get("BASE_URL", "").strip().rstrip("/"),
        "model": env.get("MODEL", "").strip(),
    }


def key_is_missing(api_key):
    """True if this is not a real key yet.

    We do not just compare against the placeholder text, because the placeholder
    tends to get edited. Anything empty, obviously a stand-in, or too short to be
    a real key counts as missing. Better to nag someone with a valid key than to
    let thirty people think they are set up when they are not.
    """
    value = (api_key or "").strip().lower()
    if not value or len(value) < 20 or "..." in value:
        return True
    return any(word in value for word in ("paste", "your-key", "xxxx", "placeholder"))


class ModelError(Exception):
    """Raised when the model server will not answer us."""


def _endpoint(base_url):
    """Most model servers answer at <base_url>/chat/completions."""
    if base_url.endswith("/chat/completions"):
        return base_url
    return base_url + "/chat/completions"


def ask(messages, tools=None, max_tokens=4000, temperature=0.3):
    """Send a conversation to the model and return its reply.

    `messages` is a list like:
        [{"role": "system",    "content": "You are a legal assistant."},
         {"role": "user",      "content": "What should I do?"},
         {"role": "assistant", "content": "I would first read the contract."}]

    That list is the model's entire world. It has no memory of anything
    that is not in it - which is exactly why memory.yaml exists.

    `tools` is the list of things the model is allowed to ask for. See
    harness/tools.py. If we pass it, the model can reply with a tool call
    instead of (or as well as) ordinary text.

    We get back a dictionary:

        {"text":       what the model said out loud,
         "thinking":   its reasoning before answering,
         "tool_calls": the things it wants the harness to do,
         "cut_off":    True if it ran out of room mid-sentence,
         "tokens":     what this call cost, in tokens}

    The model we are using thinks before it answers, and the server sends
    that thinking back separately. During the loop the model usually says
    almost nothing out loud - it thinks, then it calls a tool - so the
    thinking is the interesting part to watch.
    """
    cfg = settings()

    if key_is_missing(cfg["api_key"]):
        raise ModelError(
            "No API key found.\n"
            "   Open the file .env and paste your key after API_KEY=\n"
            "   You make a key at https://platform.ifm.ai/"
        )
    if not cfg["base_url"]:
        raise ModelError("BASE_URL is missing from your .env file.")
    if not cfg["model"]:
        raise ModelError("MODEL is missing from your .env file.")

    payload = {
        "model": cfg["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        payload["tools"] = tools
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        _endpoint(cfg["base_url"]),
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + cfg["api_key"],
        },
        method="POST",
    )

    # Try twice. Model servers occasionally hiccup and a single retry
    # saves a lot of frustration in a room full of people.
    last_error = None
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(request, timeout=240) as response:
                result = json.loads(response.read().decode("utf-8"))
            choice = result["choices"][0]
            reply = choice["message"]
            usage = result.get("usage") or {}
            return {
                "text": (reply.get("content") or "").strip(),
                "thinking": (reply.get("reasoning_content") or reply.get("reasoning") or "").strip(),
                "tool_calls": _read_tool_calls(reply.get("tool_calls")),
                "cut_off": choice.get("finish_reason") == "length",
                "tokens": usage.get("total_tokens") or 0,
            }
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")[:400]
            if err.code in (401, 403):
                raise ModelError(
                    "The model server rejected your API key (error %s).\n"
                    "   Check for a stray space or a missing character in .env."
                    % err.code
                )
            if err.code == 404:
                raise ModelError(
                    "The model server said 'not found' (404).\n"
                    "   Check BASE_URL and MODEL in your .env file.\n"
                    "   Server said: %s" % detail
                )
            if err.code == 429:
                raise ModelError(
                    "Too many requests at once (429). Wait ten seconds and run it again."
                )
            last_error = ModelError("Model server error %s: %s" % (err.code, detail))
        except urllib.error.URLError as err:
            last_error = ModelError(
                "Could not reach the model server.\n"
                "   Check your internet connection and BASE_URL in .env.\n"
                "   Details: %s" % err.reason
            )
        except (KeyError, IndexError, ValueError) as err:
            last_error = ModelError("The model server sent back something unexpected: %s" % err)

        if attempt == 1:
            time.sleep(2)

    raise last_error


def _read_tool_calls(raw):
    """Turn the server's tool calls into something easier to work with.

    The server sends the arguments as a string of JSON, so we unpack it.
    """
    calls = []
    for item in raw or []:
        function = item.get("function") or {}
        try:
            arguments = json.loads(function.get("arguments") or "{}")
        except ValueError:
            arguments = {}
        calls.append(
            {
                "id": item.get("id", ""),
                "name": function.get("name", ""),
                "arguments": arguments if isinstance(arguments, dict) else {},
                "raw": item,
            }
        )
    return calls


def assistant_message(reply):
    """Rebuild the model's turn so it can be sent back in the next request.

    Every request carries the whole conversation, so the model's own turns
    have to go back in too - including its thinking, which this particular
    server requires.
    """
    message = {"role": "assistant", "content": reply["text"], "reasoning_content": reply["thinking"]}
    if reply["tool_calls"]:
        message["tool_calls"] = [call["raw"] for call in reply["tool_calls"]]
    return message


def tool_result_message(call, result):
    """The message that hands a tool's output back to the model."""
    return {"role": "tool", "tool_call_id": call["id"], "content": result}
