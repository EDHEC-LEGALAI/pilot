# Internal know-how note - AI in recruitment (EU and France)

*Kept by the firm's technology and employment teams. A summary for orientation,
not a substitute for checking the current text. **Verify whether any amending
instrument has changed the application dates before advising** - the timetable
below has been the subject of legislative proposals.*

---

## 1. Regulation (EU) 2024/1689 (the AI Act)

**Roles.** The *provider* develops and places the system on the market. The
*deployer* uses it under its own authority. A company that buys a tool and uses it
is normally a deployer. **Article 25** turns a deployer into a provider if it puts
its own name or trade mark on the system, makes a *substantial modification*, or
changes the intended purpose.

**Application dates (as enacted).**
- In force 1 August 2024.
- **Prohibited practices (Art. 5) and AI literacy (Art. 4): 2 February 2025.**
- General purpose AI, governance, penalties: 2 August 2025.
- **Annex III high-risk obligations: 2 August 2026.**
- Art. 6(1) high-risk (safety components of regulated products): 2 August 2027.

**Prohibited practices - Article 5(1)(f).** It is prohibited to put into service or
use AI systems **to infer emotions of a natural person in the areas of workplace
and education institutions**, save for medical or safety reasons. Recital 44
explains the concern: unreliability, and the power imbalance in employment. The
Commission's guidelines on prohibited practices treat the recruitment and
probation stages as falling within "the workplace". Breach attracts the highest
tier of fines (up to EUR 35m or 7% of worldwide turnover).

**High risk - Annex III point 4(a).** AI systems intended to be used for
recruitment or selection, **in particular to analyse and filter job applications
and to evaluate candidates**, are high-risk.

**The Article 6(3) escape route, and its limit.** An Annex III system is not
high-risk if it performs only a narrow procedural task, or improves the result of
a previously completed human activity, or is preparatory, and does not pose a
significant risk. **But the final sub-paragraph of Article 6(3) provides that a
system is ALWAYS high-risk where it performs profiling of natural persons.** A
provider relying on the derogation must document its assessment (Art. 6(4)).

**Deployer obligations for high-risk systems - Article 26.** In outline:
- use it in accordance with the instructions for use;
- **assign human oversight to natural persons who have the competence, training
  and authority, and the necessary support** (Art. 26(2));
- ensure input data is relevant and sufficiently representative (Art. 26(4));
- monitor operation, and suspend use and inform the provider and the market
  surveillance authority where a risk or serious incident arises (Art. 26(5));
- keep logs for at least six months (Art. 26(6));
- **before putting a high-risk system into use at the workplace, an employer
  deployer must inform workers' representatives and the affected workers**
  (Art. 26(7));
- **inform individuals that they are subject to the system** where it is used to
  make or assist decisions about them (Art. 26(11)).

**Article 86** gives a person affected by a decision taken on the basis of the
output of an Annex III high-risk system the right to a **clear and meaningful
explanation** of the role of the system in the decision.

**CE marking (Art. 48)** applies to high-risk AI systems. A CE mark on a system
the provider says is *not* high-risk is a question worth asking.

---

## 2. GDPR

**Article 22.** A person has the right not to be subject to a decision based
**solely** on automated processing which produces legal effects or **similarly
significantly affects** them. Regulatory guidance treats automated rejection in
e-recruitment as within this. Exceptions: necessary for a contract, authorised by
Union or Member State law, or explicit consent - and consent is fragile in an
employment context because of the imbalance of power. Where an exception applies,
**safeguards are mandatory: at minimum the right to obtain human intervention, to
express a point of view and to contest the decision.**

**"Solely".** Human involvement must be meaningful - a real review by someone with
the authority and information to change the outcome. A human who never sees the
candidate is not involvement.

**Article 35.** A DPIA is required for systematic and extensive evaluation based
on automated processing, including profiling, on which decisions are based that
significantly affect the person. The CNIL's list also captures it.

**Article 9.** Inferences about health, disability or ethnic origin are special
category data even if never asked for. Behavioural inference from video, and
location-derived signals, both raise this.

**Articles 13-14.** Where Article 22 applies, the individual must be given
meaningful information about the logic involved and the significance and envisaged
consequences.

**Controller and processor.** A vendor that reuses client data to improve its own
product is determining purposes for that processing and is a controller for it,
whatever the DPA says on its front page.

---

## 3. French law

- **Art. L.1221-8 and L.1221-9 Code du travail.** A candidate must be informed in
  advance of the methods and techniques of recruitment used; results are
  confidential; the methods must be **relevant to the job applied for**.
- **Art. L.1222-4.** No information may be collected about a person by a device
  that has not been brought to their knowledge beforehand.
- **Art. L.2312-8 and L.2312-38 Code du travail.** The CSE must be informed and
  consulted on the introduction of new technologies and **before any decision to
  implement automated processing for personnel management**. Consultation is
  before the decision, not after. Proceeding without it exposes the company to
  suspension of the project and to *délit d'entrave*.
- **Art. L.1132-1.** Non-discrimination. A statistically "neutral" outcome on one
  protected characteristic does not answer the question for others.
- The CNIL has published guidance on recruitment; the Défenseur des droits has
  taken an active interest in algorithmic recruitment.
