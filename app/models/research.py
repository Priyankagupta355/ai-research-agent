from pydantic import BaseModel
from typing import List

class ResearchSource(BaseModel):
    title: str
    url: str


class ResearchReport(BaseModel):
    title: str
    summary: str
    key_findings: List[str]
    sources: List[ResearchSource]
    conclusion: str
