# 🎓 Counselor Co-Pilot

> An AI-assisted prep tool that turns K-12 student data into counselor-ready briefs in seconds.

**Try the live demo:** *(deploy link coming next step)*

---

## The problem

K-12 counselors typically support 300–500 students each. Before every meeting, they have to mentally stitch together attendance, grades, behavior flags, college application progress, and career interests from multiple systems — often in the 5 minutes between back-to-back appointments.

The data exists. The time to synthesize it doesn't.

## What this prototype does

Counselor Co-Pilot reads a student's record and produces a short, actionable brief:

> *"Mateo is off to a strong start academically, maintaining a 3.7 GPA... However, his attendance rate of 87.9% indicates some potential challenges with punctuality and engagement. One concern that needs attention is the two behavior flags this quarter... Given his career interest in Education, it would be beneficial to explore pathways that align with this goal..."*

Not a dashboard. Not a chatbot. A **counselor-ready brief** that surfaces what to talk about, in plain English, in under 20 seconds.

## Why this design

A few intentional choices:

- **The AI proposes, the counselor decides.** Every brief ends with a reminder that AI augments judgment, it doesn't replace it.
- **Constrained outputs.** The prompt enforces a fixed structure (status → concern → next conversation → pathway action) so briefs stay scannable, not rambly.
- **Synthetic data only.** No real student PII goes anywhere near this prototype. Production deployment would require FERPA-compliant infrastructure.
- **NIST AI RMF alignment.** Transparency, human oversight, and risk minimization are surfaced in the UI itself, not buried in docs.

## Tech stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Language | Python 3.14 |
| LLM | Hugging Face Inference Providers (Llama 3.1 8B Instruct) |
| Data | Pandas + synthetic generator |
| Secrets | python-dotenv |

## Project structure
counselor-copilot/
├── app.py                    # Streamlit UI
├── src/
│   ├── data_generator.py     # Synthetic student data
│   └── summarize.py          # LLM prompt + API call
├── data/
│   └── sample_students.csv   # 50 synthetic students
├── requirements.txt
├── .env.example              # Template for secrets
└── README.md
## Run it locally

```bash
git clone https://github.com/dikshanegi12/counselor-copilot.git
cd counselor-copilot
python -m venv venv
.\venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env             # then add your HF token
python src/data_generator.py     # generate sample data
streamlit run app.py
```

## What I'd build next

This is a weekend prototype. With more time, the natural next steps:

1. **Counselor feedback loop** — let counselors rate briefs and use that signal to refine the prompt
2. **Cohort view** — surface patterns across a counselor's full caseload ("8 of your 11th graders haven't started college apps")
3. **Pathway data integration** — connect to actual dual-credit / CTE catalogs so suggestions are real, not generic
4. **Bias auditing** — sample briefs across demographic slices to check for differential treatment in tone or recommendations
5. **Counselor-in-the-loop fine-tuning** — once we have enough rated briefs, move from prompt engineering to a small fine-tuned model

## A note on AI in K-12

The temptation with AI in education is to automate decisions. The opportunity is to **buy counselors back time** so they can have more, deeper, more informed human conversations with students.

This prototype is built around that distinction.

---

*Built as a weekend prototype to explore AI augmentation in college and career advising workflows.*