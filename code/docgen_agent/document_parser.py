"""
Document parser agent for legal documents.
"""

import logging
import re
from typing import Annotated, Any, Sequence

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from .models import LegalDocument

_LOGGER = logging.getLogger(__name__)

llm = ChatNVIDIA(model="meta/llama-3.1-8b-instruct", temperature=0)


class DocumentParserState(BaseModel):
    content: str
    title: str = "Unknown Document"
    document_type: str = "Terms of Service"
    parsed_document: LegalDocument | None = None
    messages: Annotated[Sequence[Any], add_messages] = []


def extract_sections(content: str) -> list[dict]:
    """Extract sections from legal document content."""
    sections = []

    # Split by common section headers
    section_patterns = [
        r"\d+\.\s*([^.\n]+)",  # 1. Section Title
        r"[A-Z][A-Z\s]+\n",  # ALL CAPS HEADERS
        r"^[A-Z][a-z\s]+:$",  # Title Case: headers
    ]

    lines = content.split("\n")
    current_section = {"title": "Introduction", "content": ""}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a section header
        is_header = False
        for pattern in section_patterns:
            if re.match(pattern, line):
                if current_section["content"].strip():
                    sections.append(current_section)
                current_section = {"title": line, "content": ""}
                is_header = True
                break

        if not is_header:
            current_section["content"] += line + "\n"

    # Add the last section
    if current_section["content"].strip():
        sections.append(current_section)

    return sections


def parse_legal_document(state: DocumentParserState, config: RunnableConfig):
    """Parse and structure the legal document."""
    _LOGGER.info("Parsing legal document: %s", state.title)

    # Extract sections
    sections = extract_sections(state.content)

    # Create structured document
    parsed_document = LegalDocument(
        title=state.title,
        content=state.content,
        document_type=state.document_type,
        sections=sections,
    )

    return {"parsed_document": parsed_document, "messages": state.messages}


# Create the workflow graph
def create_graph():
    """Create the document parsing workflow."""
    workflow = StateGraph(DocumentParserState)

    # Add nodes
    workflow.add_node("parse_legal_document", parse_legal_document)

    # Add edges
    workflow.add_edge(START, "parse_legal_document")
    workflow.add_edge("parse_legal_document", END)

    return workflow.compile()


# Create the graph instance
graph = create_graph()
