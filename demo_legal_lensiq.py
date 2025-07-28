#!/usr/bin/env python3
"""
LegalLensIQ Demo Script for Hackathon Presentation
"""

import sys
import os
import time

# Add the code directory to Python path
code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'code')
sys.path.insert(0, code_dir)

def print_header():
    """Print the demo header."""
    print("=" * 60)
    print("🔍 LegalLensIQ - Terms of Service Analyzer")
    print("=" * 60)
    print("Built with NVIDIA's AgentIQ Toolkit")
    print("Analyzing legal documents for risks and compliance")
    print("=" * 60)
    print()

def demo_high_risk_document():
    """Demo with a high-risk document."""
    print("📄 Document 1: High-Risk Terms of Service")
    print("-" * 50)
    
    high_risk_tos = """
    Terms of Service
    
    1. Data Collection and Usage
    We may collect and sell your personal information to third parties for marketing purposes. We also track your browsing history across websites and collect location data.
    
    2. Account Termination
    We reserve the right to terminate your account at any time without notice or explanation. We can suspend your account without warning.
    
    3. Dispute Resolution
    All disputes must be resolved through binding arbitration. You waive your right to a jury trial or class action lawsuit. No other legal recourse is available.
    
    4. Data Retention
    We may retain your data indefinitely and store it permanently. We keep your information forever.
    
    5. Modifications
    We can modify these terms at any time without notice. We reserve the right to change these terms anytime.
    
    6. Liability
    We are not liable for any damages or losses. You waive all rights to compensation.
    
    7. No Refunds
    All sales are final. No refunds will be provided under any circumstances.
    
    By using our service, you waive all legal rights and agree to these terms.
    """
    
    from docgen_agent.risk_analyzer import detect_risk_patterns, check_compliance, calculate_fairness_score, generate_recommendations
    
    print("Analyzing document...")
    time.sleep(1)
    
    risks = detect_risk_patterns(high_risk_tos.lower())
    compliance = check_compliance(high_risk_tos.lower())
    fairness_score = calculate_fairness_score(risks, compliance)
    recommendations = generate_recommendations(risks, compliance)
    
    print(f"🎯 Fairness Score: {fairness_score}/100")
    
    if fairness_score >= 80:
        status = "✅ FAIR"
    elif fairness_score >= 60:
        status = "⚠️ MODERATE"
    else:
        status = "🚨 UNFAIR"
    print(f"Status: {status}")
    
    print(f"\n⚠️ Risk Analysis:")
    for risk_type, clauses in risks.items():
        risk_name = risk_type.replace('_', ' ').title()
        print(f"  • {risk_name}: {len(clauses)} concerning clause(s)")
    
    print(f"\n💡 Key Recommendations:")
    for rec in recommendations[:3]:  # Show top 3
        print(f"  • {rec}")
    
    print()

def demo_fair_document():
    """Demo with a fair document."""
    print("📄 Document 2: Fair Terms of Service")
    print("-" * 50)
    
    fair_tos = """
    Terms of Service
    
    1. Data Collection and Usage
    We only collect data necessary to provide our service. We do not sell your personal information to third parties. We do not track your browsing history across websites.
    
    2. Account Terms
    You can cancel your account at any time. We will provide a prorated refund for unused services. We will notify you 30 days before making any changes to these terms.
    
    3. Privacy Rights
    Under GDPR, you have the right to access, correct, and delete your data. Under CCPA, California residents can opt out of data sales. We retain your data only as long as necessary to provide our service.
    
    4. Dispute Resolution
    You can choose between arbitration and small claims court for disputes. We are liable for damages caused by our negligence.
    
    5. Data Retention
    We retain your data only as long as necessary to provide our service. We will delete your data upon request.
    
    6. Modifications
    We will notify you 30 days before making any changes to these terms. You can cancel if you don't agree to changes.
    
    7. Liability
    We are liable for damages caused by our negligence. We provide clear refund policies.
    
    8. Children's Privacy
    We do not knowingly collect data from children under 13 without parental consent.
    
    9. Contact Information
    Contact us at support@example.com for any questions about these terms.
    """
    
    from docgen_agent.risk_analyzer import detect_risk_patterns, check_compliance, calculate_fairness_score, generate_recommendations
    
    print("Analyzing document...")
    time.sleep(1)
    
    risks = detect_risk_patterns(fair_tos.lower())
    compliance = check_compliance(fair_tos.lower())
    fairness_score = calculate_fairness_score(risks, compliance)
    recommendations = generate_recommendations(risks, compliance)
    
    print(f"🎯 Fairness Score: {fairness_score}/100")
    
    if fairness_score >= 80:
        status = "✅ FAIR"
    elif fairness_score >= 60:
        status = "⚠️ MODERATE"
    else:
        status = "🚨 UNFAIR"
    print(f"Status: {status}")
    
    print(f"\n🛡️ Compliance Check:")
    for framework, clauses in compliance.items():
        framework_name = framework.upper()
        if clauses:
            print(f"  • {framework_name}: ✅ Found {len(clauses)} compliance clauses")
        else:
            print(f"  • {framework_name}: ❌ No compliance clauses")
    
    print(f"\n💡 Key Recommendations:")
    for rec in recommendations[:3]:  # Show top 3
        print(f"  • {rec}")
    
    print()

def print_summary():
    """Print the demo summary."""
    print("=" * 60)
    print("📊 LegalLensIQ Summary")
    print("=" * 60)
    print("✅ What LegalLensIQ Does:")
    print("  • Parses Terms of Service, Privacy Policies, EULAs")
    print("  • Detects risky clauses (data selling, arbitration, unfair terms)")
    print("  • Checks compliance with GDPR, COPPA, CCPA")
    print("  • Calculates fairness scores (0-100)")
    print("  • Provides actionable recommendations")
    print()
    print("🎯 Key Benefits:")
    print("  • Protects consumers from hidden risks")
    print("  • Helps businesses write compliant documents")
    print("  • Saves hours of legal review time")
    print("  • Provides instant analysis and scoring")
    print()
    print("🚀 Built with NVIDIA's AgentIQ Toolkit")
    print("  • Uses pattern matching for risk detection")
    print("  • Integrates with NVIDIA AI endpoints")
    print("  • Scalable for any legal document type")
    print("=" * 60)

def main():
    """Run the demo."""
    print_header()
    
    demo_high_risk_document()
    demo_fair_document()
    print_summary()

if __name__ == "__main__":
    main() 