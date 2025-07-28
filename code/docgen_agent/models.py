"""
Shared models for the document generation agents.
"""

from typing import Annotated, Any, Sequence

from langgraph.graph.message import add_messages
from pydantic import BaseModel


class LegalDocument(BaseModel):
    title: str
    content: str
    document_type: str  # ToS, Privacy Policy, EULA
    sections: list[dict] = []


class LegalAnalysis(BaseModel):
    document: LegalDocument
    risk_analysis: dict = {}
    compliance_check: dict = {}
    summary: str = ""
    fairness_score: int = 0
    recommendations: list[str] = []
    messages: Annotated[Sequence[Any], add_messages] = []


class LegalAgentState(BaseModel):
    document_content: str
    document_title: str = "Unknown Document"
    document_type: str = "Terms of Service"
    parsed_document: LegalDocument | None = None
    risk_analysis: dict = {}
    compliance_check: dict = {}
    summary: str = ""
    fairness_score: int = 0
    recommendations: list[str] = []
    messages: Annotated[Sequence[Any], add_messages] = [] 