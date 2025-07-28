# LegalLensIQ - Intelligent Terms of Service Analyzer

🚀 **AI-powered legal document analysis that helps users understand what they're actually agreeing to.**

## 🚀 Features

- **Automated Risk Detection:** Identifies unfair clauses using pattern matching
- **Fairness Scoring:** 0-100 score based on legal best practices
- **Interactive Chatbot:** Ask questions about specific documents
- **Real-time Analysis:** Instant results with detailed explanations
- **Privacy Rights Guidance:** GDPR, CCPA, and consumer protection

## 🛠️ Technology Stack

- **Frontend:** HTML/CSS/JavaScript
- **Backend:** Python HTTP Server
- **AI:** NVIDIA AgentIQ Toolkit (optional)
- **Pattern Matching:** Enhanced regex for legal clause detection

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

3. **Set up API keys (optional for LLM features):**
   ```bash
   cp secrets.env.example secrets.env
   # Edit secrets.env with your API keys (do NOT commit this file)
   ```

4. **Run the web server:**
   ```bash
   python server.py
   ```

5. **Open in browser:**
   ```
   http://localhost:8000
   ```

## 📊 How the Fairness Score Works

- **Base Score:** 100 points
- **Risk Deductions:**
  - Broad Liability Waivers: -30
  - Data Selling: -30
  - Mandatory Arbitration: -25
  - Excessive Data Collection: -25
  - Extensive Data Sharing: -25
  - Lack of User Control: -25
  - Waiver of Rights: -20
  - Broad Termination Rights: -20
  - Indefinite Data Retention: -20
  - Broad Data Use: -20
  - Unilateral Changes: -15
  - Sole Discretion Clauses: -15
  - Automatic Renewal: -15
  - No Refunds: -10
- **Compliance Bonuses:**
  - Fair Terms: +15
  - Privacy Best Practices: +15
  - GDPR: +10
  - CCPA: +10
  - COPPA: +10
- **Score Ranges:**
  - 80-100: ✅ FAIR
  - 60-79: ⚠️ MODERATE
  - 0-59: 🚨 UNFAIR

## 🛡️ Security & API Keys

- **Never commit your real API keys!**
- `secrets.env` is in `.gitignore` and will not be committed.
- Use `secrets.env.example` as a template for sharing.

## 📋 Demo Usage

1. **Load the Interface:** Run `python3 server.py` or open `index.html`
2. **Enter Document:** Paste your Terms of Service or use the sample
3. **Click Analyze:** See fairness score, risks, compliance, and recommendations
4. **Chatbot:** Ask questions about the document, risks, or legal terms

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional risk patterns
- More compliance frameworks
- Enhanced chatbot responses
- Mobile app development

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with NVIDIA's AgentIQ Toolkit
- Inspired by consumer protection needs
- Designed for hackathon demonstration


