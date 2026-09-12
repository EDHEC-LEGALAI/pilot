# TalentSift - Product description (vendor documentation, v4.2)

**Vendor:** Corvid Labs GmbH, Munich
**Product:** TalentSift Recruitment Intelligence Platform

## What it does

TalentSift ingests applications from your careers site and applicant tracking
system and produces a ranked shortlist for each vacancy.

### Module 1 - Parse
Extracts structured data from CVs in 14 languages: education, employers, dates,
certifications, licence numbers, gaps in employment history.

### Module 2 - Score (core)
Produces a **Fit Score from 0 to 100** for each candidate against the vacancy.
The model was trained on **4.1 million historical applications and the hiring and
retention outcomes associated with them**, drawn from our client base since 2017.

Configurable behaviour:
- **Auto-advance** candidates scoring above a threshold you set.
- **Auto-reject** candidates scoring below a threshold you set. Rejected
  candidates receive a templated email. *Recommended threshold: 55.*
- **Review queue** for everyone in between.

Clients typically report a **71% reduction in recruiter screening time**.

### Module 3 - Signals (optional add-on)
Adds predictive signals to the Fit Score:
- *Stability signal* - likelihood the candidate remains in post beyond 12 months,
  inferred from employment history patterns and postcode-level data.
- *Engagement signal* - derived from the candidate's asynchronous video interview:
  analyses **facial expression, vocal tone and speech pacing** to estimate
  enthusiasm and confidence.

### Module 4 - Explain
Generates a one-line reason for each ranking, e.g. *"Strong match on paediatric
certification; limited recent acute experience."*

## Deployment

Hosted in Corvid Labs' Frankfurt region. Data retained for 24 months. Model
retrained quarterly on aggregated client outcome data unless the client opts out
in writing.
