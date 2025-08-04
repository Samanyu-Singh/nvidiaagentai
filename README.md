# LegalLensIQ - Intelligent Terms of Service Analyzer

🚀 **AI-powered legal document analysis that helps users understand what they're actually agreeing to.**

## 🚀 Features

- **Automated Risk Detection:** Identifies unfair clauses using pattern matching
- **Fairness Scoring:** 0-100 score based on legal best practices
- **Interactive Chatbot:** Ask questions about specific documents
- **Real-time Analysis:** Instant results with detailed explanations
- **Privacy Rights Guidance:** GDPR, CCPA, and consumer protection
- **Document Analysis:** Comprehensive legal document parsing and analysis

## 🛠️ Technology Stack

- **Frontend:** HTML/CSS/JavaScript
- **Backend:** Python HTTP Server
- **AI:** NVIDIA AI Endpoints (Llama 3.1 8B)
- **Pattern Matching:** Enhanced regex for legal clause detection
- **Document Processing:** PDF parsing and text extraction

## 🎯 Use Cases

- **Consumer Protection:** Understand Terms of Service before agreeing
- **Privacy Analysis:** Check data collection and sharing practices
- **Legal Education:** Learn about your rights and unfair practices
- **Document Comparison:** Compare different service agreements

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/legal-lens-iq.git
   cd legal-lens-iq
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up NVIDIA API key:**
   ```bash
   cp secrets.env.example secrets.env
   # Edit secrets.env with your NVIDIA API key (do NOT commit this file)
   ```

4. **Run the web server:**
   ```bash
   python server.py
   ```

5. **Open in browser:**
   ```
   http://localhost:8081
   ```

## 📊 How the Fairness Score Works

- **Base Score:** 100 points
- **Risk Deductions:**
  - Data Selling: -45 (extremely problematic)
  - Extensive Data Sharing: -40 (major privacy concern)
  - Excessive Data Collection: -30 (significant concern)
  - Broad Data Use: -30 (significant concern)
  - Lack of User Control: -25 (varies by service)
  - Indefinite Data Retention: -20 (problematic but common)
  - Broad Liability Waivers: -18 (standard business practice)
  - Waiver of Rights: -18 (concerning but standard)
  - Mandatory Arbitration: -12 (common for tech companies)
  - Broad Termination Rights: -15 (reasonable for service providers)
  - Unilateral Changes: -8 (standard practice)
  - Sole Discretion Clauses: -8 (common business practice)
  - Automatic Renewal: -8 (common subscription model)
  - No Refunds: -6 (minor issue)
- **Compliance Bonuses:**
  - Fair Terms: +25
  - Privacy Best Practices: +25
  - GDPR: +18
  - CCPA: +15
  - COPPA: +15
- **Score Ranges:**
  - 80-100: ✅ FAIR
  - 60-79: ⚠️ MODERATE
  - 0-59: 🚨 UNFAIR

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with NVIDIA's AI Endpoints
- Inspired by consumer protection needs
- Designed for hackathon demonstration


