"""
Risk analyzer agent for legal documents.
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


class RiskAnalyzerState(BaseModel):
    document: LegalDocument
    risk_analysis: dict = {}
    compliance_check: dict = {}
    fairness_score: int = 0
    recommendations: list[str] = []
    messages: Annotated[Sequence[Any], add_messages] = []


# Enhanced risk patterns to catch sophisticated unfair terms
RISK_PATTERNS = {
    "mandatory_arbitration": [
        r"arbitration.*shall.*determined",
        r"mandatory.*arbitration",
        r"binding.*arbitration",
        r"arbitration.*before.*arbitrator",
        r"JAMS.*arbitration",
        r"arbitration.*rules.*procedures",
        r"judgment.*award.*court",
        r"no.*right.*sue.*court",
        r"waive.*right.*jury.*trial",
    ],
    "broad_liability_waivers": [
        r"no.*liability.*damages",
        r"limited.*liability.*maximum",
        r"not.*liable.*any.*damages",
        r"disclaim.*all.*warranties",
        r"as.*is.*as.*available",
        r"with.*all.*faults",
        r"consequential.*damages",
        r"punitive.*damages",
        r"exemplary.*damages",
        r"lost.*profits.*data",
        r"business.*reputation",
        r"intangible.*loss",
    ],
    "broad_termination_rights": [
        r"terminate.*account.*without.*notice",
        r"suspend.*account.*sole.*discretion",
        r"delete.*account.*discretion",
        r"violation.*terms.*terminate",
        r"infringement.*rights.*terminate",
        r"applicable.*laws.*terminate",
        r"might.*constitute.*violation",
        r"would.*constitute.*violation",
    ],
    "automatic_renewal": [
        r"automatically.*renew",
        r"auto.*renewal",
        r"renew.*end.*period",
        r"unless.*cancel.*before",
        r"recurring.*subscription",
        r"continuous.*billing",
    ],
    "excessive_data_collection": [
        r"location.*data",
        r"birth.*date.*photo",
        r"ID.*photo",
        r"personal.*data.*collect",
        r"cookies.*tracking",
        r"user.*information.*collect",
        r"browsing.*history",
        r"device.*information",
        r"biometric.*identifiers",
        r"faceprints.*voiceprints",
        r"keystroke.*patterns",
        r"clipboard.*information",
        r"social.*network.*contacts",
        r"phone.*contacts",
        r"precise.*location",
        r"GPS.*information",
        r"metadata.*upload",
        r"device.*identifiers",
        r"advertising.*identifiers",
        r"IP.*address.*geolocation",
    ],
    "no_refunds": [
        r"no.*refunds",
        r"non.*refundable",
        r"all.*sales.*final",
        r"no.*money.*back",
        r"subscription.*non.*refundable",
    ],
    "data_selling": [
        r"sell.*personal.*information",
        r"share.*data.*third.*parties",
        r"transfer.*data.*marketing",
        r"disclose.*user.*information",
        r"data.*marketing.*purposes",
        r"advertisers.*share.*information",
        r"business.*partners.*share",
        r"cross.*context.*behavioral.*advertising",
        r"targeted.*advertising",
        r"personalized.*advertising",
    ],
    "unilateral_changes": [
        r"change.*terms.*any.*time",
        r"modify.*agreement.*notice",
        r"update.*terms.*discretion",
        r"reserve.*right.*change",
        r"alter.*replace.*modify",
        r"update.*privacy.*policy.*time",
    ],
    "sole_discretion_clauses": [
        r"sole.*discretion",
        r"our.*discretion",
        r"company.*discretion",
        r"reasonable.*discretion",
        r"appropriate.*circumstances",
    ],
    "waiver_of_rights": [
        r"waive.*all.*rights",
        r"waive.*legal.*rights",
        r"waive.*claims",
        r"irrevocably.*waive",
        r"waive.*any.*claim",
    ],
    "extensive_data_sharing": [
        r"share.*with.*service.*providers",
        r"share.*with.*business.*partners",
        r"share.*with.*advertisers",
        r"share.*with.*third.*parties",
        r"corporate.*group.*entities",
        r"affiliated.*entities",
        r"global.*company",
        r"international.*transfer",
        r"cross.*border.*transfer",
        r"servers.*outside.*united.*states",
    ],
    "indefinite_data_retention": [
        r"retain.*as.*long.*necessary",
        r"retain.*legitimate.*business.*interest",
        r"retain.*legal.*obligations",
        r"retain.*defense.*legal.*claims",
        r"retain.*improve.*develop",
        r"retain.*safety.*security",
        r"retain.*violation.*terms",
        r"keep.*information.*violation",
        r"retention.*different.*criteria",
        r"keep.*account.*long.*account",
    ],
    "broad_data_use": [
        r"use.*advertising.*marketing",
        r"use.*targeted.*advertising",
        r"use.*personalized.*content",
        r"use.*infer.*information",
        r"use.*demographic.*classification",
        r"use.*content.*recommendations",
        r"use.*ad.*recommendations",
        r"use.*machine.*learning",
        r"use.*AI.*training",
        r"use.*algorithm.*improvement",
        r"use.*research.*purposes",
        r"use.*analytics.*measurement",
    ],
    "lack_of_user_control": [
        r"no.*opt.*out.*data.*collection",
        r"cannot.*opt.*out.*tracking",
        r"required.*data.*collection",
        r"necessary.*for.*service",
        r"cannot.*disable.*cookies",
        r"cannot.*disable.*tracking",
        r"cannot.*delete.*account",
        r"cannot.*remove.*data",
        r"limited.*data.*deletion",
        r"partial.*data.*removal",
    ],
}

# Enhanced compliance patterns
COMPLIANCE_PATTERNS = {
    "gdpr": [
        r"right.*to.*deletion",
        r"data.*portability",
        r"explicit.*consent",
        r"data.*processing.*basis",
        r"privacy.*policy",
        r"data.*protection",
        r"personal.*data.*rights",
        r"lawful.*basis.*processing",
        r"data.*subject.*rights",
        r"privacy.*by.*design",
    ],
    "coppa": [
        r"children.*under.*13",
        r"parental.*consent",
        r"collect.*child.*data",
        r"age.*verification",
        r"minor.*protection",
        r"children.*privacy.*policy",
        r"guardian.*guide",
        r"parent.*controls",
    ],
    "ccpa": [
        r"california.*privacy",
        r"opt.*out.*sale",
        r"right.*to.*know",
        r"data.*disclosure",
        r"privacy.*rights.*act",
        r"california.*resident",
        r"personal.*information.*request",
        r"data.*access.*request",
    ],
    "fair_terms": [
        r"reasonable.*notice",
        r"due.*process",
        r"appeal.*rights",
        r"dispute.*resolution",
        r"mediation",
        r"fair.*terms",
        r"user.*control",
        r"data.*minimization",
        r"purpose.*limitation",
        r"storage.*limitation",
    ],
    "privacy_best_practices": [
        r"data.*minimization",
        r"purpose.*limitation",
        r"storage.*limitation",
        r"accuracy.*data",
        r"confidentiality.*security",
        r"accountability",
        r"transparency",
        r"user.*consent",
        r"opt.*in.*consent",
        r"granular.*consent",
    ],
}


def detect_risk_patterns(content: str) -> dict:
    """Detect risk patterns in legal document content."""
    risks = {}
    content_lower = content.lower()

    for risk_type, patterns in RISK_PATTERNS.items():
        found_clauses = []
        for pattern in patterns:
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end].strip()
                found_clauses.append(
                    {"pattern": pattern, "match": match.group(), "context": context}
                )

        if found_clauses:
            risks[risk_type] = found_clauses

    return risks


def check_compliance(content: str) -> dict:
    """Check compliance with legal frameworks."""
    compliance = {}
    content_lower = content.lower()

    for framework, patterns in COMPLIANCE_PATTERNS.items():
        found_clauses = []
        for pattern in patterns:
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()
                found_clauses.append(
                    {"pattern": pattern, "match": match.group(), "context": context}
                )

        if found_clauses:
            compliance[framework] = found_clauses

    return compliance


def calculate_fairness_score(risks: dict, compliance: dict) -> int:
    """Calculate fairness score based on risks and compliance."""
    base_score = 100

    # Risk deductions (enhanced for sophisticated unfair terms)
    risk_deductions = {
        "mandatory_arbitration": 25,  # Major deduction for arbitration
        "broad_liability_waivers": 30,  # Major deduction for liability waivers
        "broad_termination_rights": 20,  # Significant deduction
        "automatic_renewal": 15,  # Moderate deduction
        "excessive_data_collection": 25,  # Major deduction for privacy violations
        "no_refunds": 10,  # Minor deduction
        "data_selling": 30,  # Major deduction for data selling
        "unilateral_changes": 15,  # Moderate deduction
        "sole_discretion_clauses": 15,  # Moderate deduction
        "waiver_of_rights": 20,  # Significant deduction
        "extensive_data_sharing": 25,  # Major deduction for extensive sharing
        "indefinite_data_retention": 20,  # Significant deduction
        "broad_data_use": 20,  # Significant deduction
        "lack_of_user_control": 25,  # Major deduction for lack of control
    }

    # Compliance bonuses
    compliance_bonuses = {
        "gdpr": 10,
        "coppa": 10,
        "ccpa": 10,
        "fair_terms": 15,
        "privacy_best_practices": 15,
    }

    # Apply risk deductions
    for risk_type, clauses in risks.items():
        if risk_type in risk_deductions:
            deduction = risk_deductions[risk_type]
            base_score -= deduction
            _LOGGER.info(
                f"Risk deduction for {risk_type}: -{deduction} points ({len(clauses)} clauses)"
            )

    # Apply compliance bonuses
    for framework, clauses in compliance.items():
        if framework in compliance_bonuses:
            bonus = compliance_bonuses[framework]
            base_score += bonus
            _LOGGER.info(
                f"Compliance bonus for {framework}: +{bonus} points ({len(clauses)} clauses)"
            )

    # Ensure score is between 0 and 100
    return max(0, min(100, base_score))


def generate_recommendations(risks: dict, compliance: dict) -> list[str]:
    """Generate recommendations based on detected risks and compliance."""
    recommendations = []

    if "mandatory_arbitration" in risks:
        recommendations.append(
            "⚠️ Remove mandatory arbitration clause - users should have right to sue in court"
        )

    if "broad_liability_waivers" in risks:
        recommendations.append(
            "⚠️ Limit liability waivers - complete immunity is unfair to users"
        )

    if "broad_termination_rights" in risks:
        recommendations.append(
            "⚠️ Add due process for account termination - vague standards are unfair"
        )

    if "automatic_renewal" in risks:
        recommendations.append(
            "⚠️ Make subscription cancellation easier - automatic renewal can be deceptive"
        )

    if "excessive_data_collection" in risks:
        recommendations.append(
            "🚨 Limit data collection to what's necessary - excessive collection violates privacy"
        )

    if "no_refunds" in risks:
        recommendations.append(
            "⚠️ Provide clear refund policies - no-refund policies can be unfair"
        )

    if "data_selling" in risks:
        recommendations.append(
            "🚨 Prohibit selling user data - this violates user trust and privacy"
        )

    if "unilateral_changes" in risks:
        recommendations.append(
            "⚠️ Require notice for material changes - unilateral changes are unfair"
        )

    if "sole_discretion_clauses" in risks:
        recommendations.append(
            "⚠️ Add objective standards - 'sole discretion' is too vague"
        )

    if "waiver_of_rights" in risks:
        recommendations.append(
            "🚨 Remove broad rights waivers - users should retain basic legal rights"
        )

    if "extensive_data_sharing" in risks:
        recommendations.append(
            "🚨 Limit data sharing - extensive sharing with third parties violates privacy"
        )

    if "indefinite_data_retention" in risks:
        recommendations.append(
            "⚠️ Set clear data retention limits - indefinite retention is unfair"
        )

    if "broad_data_use" in risks:
        recommendations.append(
            "⚠️ Limit data use to stated purposes - broad use violates user expectations"
        )

    if "lack_of_user_control" in risks:
        recommendations.append(
            "🚨 Give users control over their data - lack of control is unfair"
        )

    # Add compliance recommendations
    if "gdpr" not in compliance:
        recommendations.append("📋 Add GDPR compliance clauses for EU users")

    if "ccpa" not in compliance:
        recommendations.append("📋 Add CCPA compliance for California users")

    if "fair_terms" not in compliance:
        recommendations.append("📋 Add fair dispute resolution process")

    if "privacy_best_practices" not in compliance:
        recommendations.append("📋 Implement privacy by design principles")

    if not recommendations:
        recommendations.append("✅ Document appears to have fair terms")

    return recommendations


def analyze_legal_risks(state: RiskAnalyzerState, config: RunnableConfig):
    """Analyze legal risks in the document."""
    content = state.document.content.lower()

    # Detect risks
    risks = detect_risk_patterns(state.document.content)

    # Check compliance
    compliance = check_compliance(state.document.content)

    # Calculate fairness score
    fairness_score = calculate_fairness_score(risks, compliance)

    # Generate recommendations
    recommendations = generate_recommendations(risks, compliance)

    return {
        "risk_analysis": risks,
        "compliance_check": compliance,
        "fairness_score": fairness_score,
        "recommendations": recommendations,
        "messages": state.messages,
    }


def create_graph():
    """Create the risk analyzer workflow."""
    workflow = StateGraph(RiskAnalyzerState)
    workflow.add_node("analyze_legal_risks", analyze_legal_risks)
    workflow.add_edge(START, "analyze_legal_risks")
    workflow.add_edge("analyze_legal_risks", END)
    return workflow.compile()


graph = create_graph()
