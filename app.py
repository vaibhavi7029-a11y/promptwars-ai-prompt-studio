import os
import re
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="PromptWars AI Prompt Studio", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

class PromptRequest(BaseModel):
    prompt: str = Field(min_length=8, max_length=12000)
    goal: str = Field(default="Make the prompt clearer and more effective", max_length=1000)
    audience: str = Field(default="General audience", max_length=500)
    tone: str = Field(default="Clear and professional", max_length=100)

def analyze_prompt(prompt: str) -> dict:
    checks = {
        "Clear objective": bool(re.search(r"\b(write|create|build|explain|analyze|summarize|generate|compare|design|classify|translate|plan)\b", prompt, re.I)),
        "Context included": len(prompt.split()) >= 25,
        "Output format specified": bool(re.search(r"\b(format|table|bullet|JSON|markdown|steps|list|report)\b", prompt, re.I)),
        "Constraints included": bool(re.search(r"\b(under|at least|maximum|avoid|must|should|do not|don't|limit|include)\b", prompt, re.I)),
        "Audience identified": bool(re.search(r"\b(for|audience|beginner|expert|student|customer|developer|manager)\b", prompt, re.I)),
        "Success criteria included": bool(re.search(r"\b(criteria|accurate|success|quality|evaluate|verify|cite|source)\b", prompt, re.I)),
    }
    score = round(sum(checks.values()) / len(checks) * 100)
    suggestions = []
    if not checks["Clear objective"]: suggestions.append("Start with a precise action verb and state the exact outcome.")
    if not checks["Context included"]: suggestions.append("Add relevant background, input data, and why the task matters.")
    if not checks["Output format specified"]: suggestions.append("Specify the desired output format, structure, and level of detail.")
    if not checks["Constraints included"]: suggestions.append("Add boundaries such as length, scope, exclusions, or required elements.")
    if not checks["Audience identified"]: suggestions.append("Identify who the response is for and their knowledge level.")
    if not checks["Success criteria included"]: suggestions.append("Define what a good answer must achieve and how facts should be checked.")
    return {"score": score, "checks": checks, "suggestions": suggestions}

def build_optimized_prompt(req: PromptRequest) -> str:
    return f"""ROLE
You are an expert assistant for the task below. Be accurate, practical, and transparent about uncertainty.

TASK
{req.goal}

ORIGINAL REQUEST
{req.prompt}

CONTEXT AND AUDIENCE
Audience: {req.audience}
Tone: {req.tone}

INSTRUCTIONS
1. Identify the requested outcome before answering.
2. Use the supplied context; do not invent missing facts.
3. If essential information is missing, state the assumption or ask one focused clarification.
4. Organize the answer into clear, useful sections.
5. Follow the requested format and constraints. Avoid irrelevant filler.

QUALITY CHECK
Before finalizing, check that the response directly addresses the task, is internally consistent, and clearly labels uncertainty.
If the task requires facts that may be current or specialized, identify what needs verification rather than fabricating details."""

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "ok", "service": "PromptWars AI Prompt Studio"}

@app.post("/api/analyze")
def analyze(req: PromptRequest):
    return analyze_prompt(req.prompt)

@app.post("/api/optimize")
async def optimize(req: PromptRequest):
    optimized = build_optimized_prompt(req)
    analysis = analyze_prompt(req.prompt)
    api_key = os.getenv("GEMINI_API_KEY")
    mode = "Built-in optimizer (no API key configured)"
    if api_key:
        try:
            async with httpx.AsyncClient(timeout=25) as client:
                response = await client.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                    params={"key": api_key},
                    json={"contents": [{"parts": [{"text": "Improve this prompt while preserving its intent. Return only the improved prompt:\n\n" + optimized}]}]},
                )
                response.raise_for_status()
                candidate = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                if candidate.strip():
                    optimized = candidate.strip()
                    mode = "Gemini AI"
        except (httpx.HTTPError, KeyError, IndexError, ValueError):
            mode = "Built-in optimizer (AI provider unavailable)"
    return {"optimized_prompt": optimized, "analysis": analysis, "mode": mode}
