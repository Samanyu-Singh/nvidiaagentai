"""
The main legal document analysis agent that orchestrates the analysis workflow.
"""

import asyncio
import logging
import os
from typing import Annotated, Any, Sequence, cast

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import document_parser, risk_analyzer
from .models import LegalDocument, LegalAgentState
from .prompts import legal_analyzer_instructions

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3
_THROTTLE_LLM_CALLS = os.getenv("THROTTLE_LLM_CALLS", "0")

# Load API key from environment
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
if nvidia_api_key:
    llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)
else:
    llm = None
    _LOGGER.warning("NVIDIA_API_KEY not set. LLM features will be disabled.")


def parse_document(state: LegalAgentState, config: RunnableConfig):
    """Parse and structure the legal document."""
    _LOGGER.info("Parsing legal document.")

    parser_state = document_parser.DocumentParserState(
        content=state.document_content,
        title=state.document_title,
        document_type=state.document_type,
        messages=state.messages,
    )

    result = document_parser.graph.invoke(parser_state, config)
    
    return {
        "parsed_document": result.get("parsed_document"),
        "messages": result.get("messages", [])
    }


def analyze_risks(state: LegalAgentState, config: RunnableConfig):
    """Analyze the document for risky clauses."""
    _LOGGER.info("Analyzing document for risks.")

    if not state.parsed_document:
        raise ValueError("Document not parsed.")

    analyzer_state = risk_analyzer.RiskAnalyzerState(
        document=state.parsed_document,
        messages=state.messages,
    )

    result = risk_analyzer.graph.invoke(analyzer_state, config)
    
    return {
        "risk_analysis": result.get("risk_analysis", {}),
        "compliance_check": result.get("compliance_check", {}),
        "fairness_score": result.get("fairness_score", 0),
        "recommendations": result.get("recommendations", []),
        "messages": result.get("messages", [])
    }


def generate_summary(state: LegalAgentState, config: RunnableConfig):
    """Generate a plain English summary of the document."""
    _LOGGER.info("Generating plain English summary.")

    if not state.parsed_document:
        raise ValueError("Document not parsed.")

    if not llm:
        # Fallback to basic summary if LLM not available
        return {"summary": "LLM analysis not available. Please check NVIDIA_API_KEY."}

    system_prompt = legal_analyzer_instructions.format(
        document_type=state.document_type,
        content=state.document_content[:2000]  # Limit for context
    )

    for count in range(_MAX_LLM_RETRIES):
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please provide a plain English summary of this {state.document_type} document, highlighting any concerning clauses and explaining the risks in simple terms."}
            ] + list(state.messages)
            
            response = llm.invoke(messages, config)
            if response and response.content:
                return {"summary": response.content}
        except Exception as e:
            _LOGGER.error(f"LLM call failed (attempt {count + 1}): {e}")
        
        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    return {"summary": "Unable to generate summary due to API issues."}


def enhance_recommendations(state: LegalAgentState, config: RunnableConfig):
    """Enhance recommendations with LLM analysis."""
    _LOGGER.info("Enhancing recommendations with LLM analysis.")

    if not llm:
        return {"enhanced_recommendations": state.recommendations}

    try:
        # Create a detailed analysis prompt
        analysis_prompt = f"""
        Analyze this {state.document_type} document and provide specific, actionable recommendations.
        
        Document Content: {state.document_content[:1500]}
        
        Current Risk Analysis: {state.risk_analysis}
        Current Fairness Score: {state.fairness_score}/100
        
        Please provide:
        1. Specific recommendations for improvement
        2. Legal context for the risks found
        3. Best practices for this type of document
        4. Compliance suggestions
        
        Format as a clear, actionable list.
        """

        messages = [
            {"role": "system", "content": "You are a legal expert specializing in consumer protection and compliance."},
            {"role": "user", "content": analysis_prompt}
        ]

        response = llm.invoke(messages, config)
        if response and response.content:
            enhanced_recommendations = state.recommendations + [response.content]
            return {"enhanced_recommendations": enhanced_recommendations}
    except Exception as e:
        _LOGGER.error(f"Failed to enhance recommendations: {e}")

    return {"enhanced_recommendations": state.recommendations}


# Create the workflow graph
def create_graph():
    """Create the legal analysis workflow."""
    workflow = StateGraph(LegalAgentState)

    # Add nodes
    workflow.add_node("parse_document", parse_document)
    workflow.add_node("analyze_risks", analyze_risks)
    workflow.add_node("generate_summary", generate_summary)
    workflow.add_node("enhance_recommendations", enhance_recommendations)

    # Add edges
    workflow.add_edge(START, "parse_document")
    workflow.add_edge("parse_document", "analyze_risks")
    workflow.add_edge("analyze_risks", "generate_summary")
    workflow.add_edge("generate_summary", "enhance_recommendations")
    workflow.add_edge("enhance_recommendations", END)

    return workflow.compile()


# Create the graph instance
graph = create_graph()


def analyze_legal_document(
    content: str,
    title: str = "Unknown Document",
    document_type: str = "Terms of Service"
) -> dict:
    """Analyze a legal document and return the results."""
    
    initial_state = LegalAgentState(
        document_content=content,
        document_title=title,
        document_type=document_type,
        messages=[]
    )
    
    result = graph.invoke(initial_state)
    
    return {
        "document_title": result.document_title,
        "document_type": result.document_type,
        "risk_analysis": result.risk_analysis,
        "compliance_check": result.compliance_check,
        "summary": result.summary,
        "fairness_score": result.fairness_score,
        "recommendations": result.recommendations,
        "enhanced_recommendations": getattr(result, 'enhanced_recommendations', result.recommendations)
    } 