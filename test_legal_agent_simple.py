#!/usr/bin/env python3
"""
Simple test script for LegalLensIQ agent - pattern matching only.
"""

import sys
import os

# Add the code directory to Python path
code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'code')
sys.path.insert(0, code_dir)

def test_legal_analyzer_simple():
    """Test the legal document analyzer with pattern matching only."""
    try:
        from docgen_agent.risk_analyzer import detect_risk_patterns, check_compliance, calculate_fairness_score, generate_recommendations
        
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
        
        print("🔍 Analyzing Legal Document (Pattern Matching Only)...")
        print("=" * 60)
        
        # Analyze risks
        risks = detect_risk_patterns(sample_tos.lower())
        
        # Check compliance
        compliance = check_compliance(sample_tos.lower())
        
        # Calculate fairness score
        fairness_score = calculate_fairness_score(risks, compliance)
        
        # Generate recommendations
        recommendations = generate_recommendations(risks, compliance)
        
        print(f"📊 Analysis Results:")
        print(f"Document: Sample Terms of Service")
        print(f"Type: Terms of Service")
        print(f"Fairness Score: {fairness_score}/100")
        
        if fairness_score >= 80:
            status = "✅ FAIR"
        elif fairness_score >= 60:
            status = "⚠️ MODERATE"
        else:
            status = "🚨 UNFAIR"
        print(f"Status: {status}")
        
        if risks:
            print(f"\n⚠️ Risk Analysis:")
            for risk_type, clauses in risks.items():
                risk_name = risk_type.replace('_', ' ').title()
                print(f"- {risk_name}: {len(clauses)} concerning clause(s)")
                for clause in clauses[:2]:  # Show first 2 clauses
                    context = clause['context'][:100] + '...' if len(clause['context']) > 100 else clause['context']
                    print(f"  • \"{context}\"")
        
        if compliance:
            print(f"\n🛡️ Compliance Check:")
            for framework, clauses in compliance.items():
                framework_name = framework.upper()
                if clauses:
                    print(f"- {framework_name}: ✅ Found {len(clauses)} compliance-related clause(s)")
                else:
                    print(f"- {framework_name}: ❌ No compliance clauses found")
        
        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"- {rec}")
        
        print("\n✅ LegalLensIQ pattern matching test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing LegalLensIQ: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_legal_analyzer_simple() 