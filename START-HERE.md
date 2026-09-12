# Start here — setting up before class

**Time needed: about 10 minutes.** Please do this *before* the session. If you get
stuck, stop and email the course contact — do not spend an hour on it.

You need two accounts, both free:

1. A **GitHub account** — [github.com/signup](https://github.com/signup). This is
   where the workshop files live and where you will work.
2. An **IFM account** — [platform.ifm.ai](https://platform.ifm.ai/). This is where
   you get the key that lets your code talk to the AI model.

There is nothing to buy and nothing to install.

---

## Step 1 — Get your API key

An **API key** is a password that lets a program use a service on your behalf.
Every AI model you call from code needs one. You are about to make your own.

1. Go to **[platform.ifm.ai](https://platform.ifm.ai/)** and create an account.
2. Once you are signed in, find the **API keys** section — it is usually under a
   settings, developer or account menu.
3. Create a new key. Give it a name you will recognise, such as `edhec`.
4. **Copy it immediately and paste it somewhere you can find again.** Most
   services show a key once and never again. If you lose it, delete that key and
   make another — that is normal and costs nothing.

Your key will look something like `IFM-v1_2lf6asPs...`. It is long.

> **Treat it like a password.** Anyone with your key can spend against your
> account. Do not paste it into a chat, an email, a slide, or any file except the
> one file we tell you about in step 3.

If you cannot find where to create a key, stop and email the course contact — do
not spend twenty minutes hunting for it.

---

---

## Step 2 — Get the workshop files

Two routes. **Route A is strongly recommended** unless you already work in a
terminal.

### Route A — in your browser (recommended)

This gives you a full professional code editor running in a browser tab. Nothing
is installed on your computer.

#### Open the workspace

Click this link, signed in to GitHub:

> **https://codespaces.new/EDHEC-LEGALAI/pilot**

Press the green **Create codespace** button. Wait about a minute while it builds.

You will end up looking at Visual Studio Code — the editor that most software is
written in. On the left is the list of files. At the bottom is the *terminal*,
where you type commands.

> *If you do not see a terminal at the bottom, use the menu:
> **Terminal → New Terminal**.*

#### Step 3 — Put your key in

In the file list on the left, click the file called **`.env`**.

It looks like this:

```
API_KEY=paste-your-key-here
BASE_URL=https://api.ifm.ai/v1
MODEL=IFM/K2-Horizon-375B-A23B
```

Replace `paste-your-key-here` with the key you made in step 1. Keep everything
else exactly as it is. No spaces, no quote marks:

```
API_KEY=IFM-v1_2lf6asPsgJnJEHXuNcTEZEA...
```

It saves automatically.

> *Can't see `.env` in the file list? Click in the terminal and type
> `python3 run.py --check` — it will create the file for you, then it will
> appear on the left.*

#### Step 4 — Check it works

Click in the terminal and type this, then press Enter:

```bash
python3 run.py --check
```

You want to see:

```
  [ok] found your .env file
  [ok] API_KEY is set (ends ...789a)
  [ok] BASE_URL = https://api.ifm.ai/v1
  [ok] MODEL = IFM/K2-Horizon-375B-A23B
  [ok] the model answered: "ready"

  [ok] You are ready. Try:  python3 run.py 1
```

**That is the whole setup.** Close the tab; your work is saved. Reopen it any
time from [github.com/codespaces](https://github.com/codespaces).

---

### Route B — on your own computer

Choose this only if you would rather work locally.

#### Check you have Python

Open a terminal:

- **Mac** — press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows** — press the Windows key, type `PowerShell`, press Enter.

Type:

```bash
python3 --version
```

You want `Python 3.9` or higher. If it says the command is not found, install
Python from [python.org/downloads](https://www.python.org/downloads/) —
**on Windows, tick "Add Python to PATH" on the first screen of the installer**.

#### Get Git and the files

Type:

```bash
git --version
```

If it is not installed, get it from [git-scm.com/downloads](https://git-scm.com/downloads)
(on Mac, running `git --version` will offer to install it for you).

Then download the workshop files:

```bash
git clone https://github.com/EDHEC-LEGALAI/pilot.git
cd pilot
```

> `git clone` copies the whole project onto your computer.
> `cd` means "change directory" — it moves you into the folder you just made.
> **Every command from now on must be typed inside that folder.**

#### Steps 3 and 4 — Put your key in and check it works

```bash
python3 run.py --check
```

That creates a file called `.env`. Open it in any text editor and replace
`paste-your-key-here` with your key. Save it, then run `python3 run.py --check`
again.

---

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `command not found: python3` | Python is not installed, or not on your PATH | Install from python.org; on Windows tick "Add Python to PATH" |
| `can't open file 'run.py'` | You are in the wrong folder | Type `cd pilot` and try again |
| `you have not pasted your key into .env yet` | The placeholder text is still there | Open `.env`, replace `paste-your-key-here` |
| `the model server rejected your API key` | The key is wrong, or has a stray space | Re-copy it from platform.ifm.ai; nothing before or after it |
| `Insufficient credit` or similar | Your IFM account has no free allowance left | Tell the course contact before the session |
| `could not reach the model server` | No internet, or `BASE_URL` was changed | Check your connection; restore `BASE_URL` from `.env.example` |
| `Too many requests` | Everyone ran it at once | Wait ten seconds, run it again |

Still stuck? Email the course contact **before** the session with a screenshot of
what you typed and what came back.

---

## One rule

**Never share your API key and never put it in a file other than `.env`.**

`.env` is listed in `.gitignore`, which means it is invisible to Git and can never
be uploaded by accident. That is why the key goes there and nowhere else. Treat it
like a password, because it is one.
