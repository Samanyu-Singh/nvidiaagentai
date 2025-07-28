"""Main entry point for the report generation workflow.

This code is a simple example of how to use the report generation workflow.
"""

import logging
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from code.docgen_agent import write_report
    from code.docgen_agent.legal_agent import analyze_legal_document
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import...")
    try:
        from docgen_agent import write_report
        from docgen_agent.legal_agent import analyze_legal_document
    except ImportError as e2:
        print(f"Alternative import failed: {e2}")
        print("Please run this script from the project root directory")
        sys.exit(1)

logging.basicConfig(level=logging.INFO)

# Example legal document analysis
def test_legal_analyzer():
    """Test the legal document analyzer."""
    sample_tos = """
    Terms of Service
    
    1. Data Collection and Usage
    We may collect and sell your personal information to third parties for marketing purposes. We also track your browsing history across websites.
    
    2. Account Termination
    We reserve the right to terminate your account at any time without notice or explanation.
    
    3. Dispute Resolution
    All disputes must be resolved through binding arbitration. You waive your right to a jury trial or class action lawsuit.
    
    4. Data Retention
    We may retain your data indefinitely and store it permanently.
    
    5. Privacy Rights
    You have the right to request deletion of your data under GDPR regulations.
    
    6. Modifications
    We can modify these terms at any time without notice.
    
    7. Liability
    We are not liable for any damages or losses.
    
    8. No Refunds
    All sales are final. No refunds will be provided.
    
    9. California Privacy
    California residents have additional privacy rights under CCPA.
    
    By using our service, you waive all legal rights and agree to these terms.
    """
    
    print("🔍 Analyzing Legal Document...")
    result = analyze_legal_document(
        content=sample_tos,
        title="Sample Terms of Service",
        document_type="Terms of Service"
    )
    
    print(f"\n📊 Analysis Results:")
    print(f"Document: {result['document_title']}")
    print(f"Type: {result['document_type']}")
    print(f"Fairness Score: {result['fairness_score']}/100")
    
    if result['summary']:
        print(f"\n📝 Summary:")
        print(result['summary'])
    
    if result['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"- {rec}")
    
    if result['risk_analysis']:
        print(f"\n⚠️ Risk Analysis:")
        for risk_type, clauses in result['risk_analysis'].items():
            print(f"- {risk_type}: {len(clauses)} concerning clause(s)")
    
    if result['compliance_check']:
        print(f"\n🛡️ Compliance Check:")
        for framework, clauses in result['compliance_check'].items():
            status = "✅" if clauses else "❌"
            print(f"- {framework.upper()}: {status}")

if __name__ == "__main__":
    # Test the legal analyzer
    test_legal_analyzer()
    
    # Original report generation example
    print("\n" + "="*50)
    print("Original Report Generation Example:")
    print("="*50)
    
    result = write_report(
        topic="Discuss the advantages of using GPUs for AI training",
        report_structure="""This report type focuses on comparative analysis.

The report structure should include:
1. Introduction (no research needed)
- Brief overview of the topic area
- Context for the comparison

2. Main Body Sections:
- One dedicated section for EACH offering being compared in the user-provided list
- Each section should examine:
- Core Features (bulleted list)
- Architecture & Implementation (2-3 sentences)
- One example use case (2-3 sentences)

3. No Main Body Sections other than the ones dedicated to each offering in the user-provided list

4. Conclusion with Comparison Table (no research needed)
- Structured comparison table that:
* Compares all offerings from the user-provided list across key dimensions
* Highlights relative strengths and weaknesses
- Final recommendations""",
    )
    if result:
        print("\n\n" + result["report"] + "\n\n")
