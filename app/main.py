from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents.research_agent import run_agent


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Research Agent",
    description="AI Research Agent using Groq and Web Tools",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ResearchRequest(BaseModel):
    query: str


# ============================================================
# RESPONSE MODEL
# ============================================================

class ResearchResponse(BaseModel):
    title: str
    summary: str
    key_findings: list[str]
    sources: list[dict]
    conclusion: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Research Agent API is running"
    }


# ============================================================
# RESEARCH ENDPOINT
# ============================================================

@app.post(
    "/research",
    response_model=ResearchResponse
)
def research(request: ResearchRequest):

    report = run_agent(request.query)

    return report