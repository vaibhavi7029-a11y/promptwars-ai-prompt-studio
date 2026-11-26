# PromptWars AI Prompt Studio

A responsive prompt-engineering workbench built for the PromptWars x Echo Engineer's AI Vibeathon 2026.

## Features
- Prompt quality scoring across six transparent criteria.
- Actionable suggestions for missing prompt elements.
- Structured prompt optimizer.
- Optional Gemini API enhancement; works without an API key.
- Copy-to-clipboard export.
- FastAPI backend, responsive frontend, Docker support and tests.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```
Open http://127.0.0.1:8000

## Optional Gemini integration
Set `GEMINI_API_KEY` as an environment variable. Never commit API keys. The app works in built-in mode without one.

## Tests
```bash
pip install pytest
pytest -q
```

## Deploy to Google Cloud Run
Enable Cloud Run and Cloud Build, install/authenticate the Google Cloud CLI, then run:
```bash
gcloud run deploy promptwars-ai-prompt-studio --source . --region asia-south1 --allow-unauthenticated
```
Copy the generated HTTPS URL into Hack2Skill's Deployed Link field.

## Evaluation alignment
| Criterion | Implementation |
|---|---|
| Code Quality | Small FastAPI app and clear naming |
| Security | API key from environment; bounded inputs; non-root Docker user |
| Efficiency | Lightweight dependencies and deterministic local analysis |
| Testing | API and utility tests |
| Accessibility | Labels, live status announcements, keyboard controls, responsive layout |
| Problem alignment / impact | Helps users inspect and improve AI prompts |

## Submission note
Confirm the exact challenge dropdown option and full brief on Hack2Skill before submitting; this repository is a prompt-engineering tool, not a claim about an unseen task brief.
