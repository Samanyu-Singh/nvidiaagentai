# LegalLensIQ - AI-Powered Terms of Service Analyzer

🔍 **Intelligent legal document analysis that helps users understand what they're actually agreeing to.**

LegalLensIQ is a sophisticated AI-powered platform that analyzes Terms of Service and Privacy Policies to identify unfair clauses, assess compliance with privacy regulations, and provide actionable recommendations. Built with NVIDIA's AgentIQ Toolkit and modern web technologies.

## 🚀 Features

<<<<<<< main
- **Automated Risk Detection:** Identifies unfair clauses using pattern matching
- **Fairness Scoring:** 0-100 score based on legal best practices
- **Interactive Chatbot:** Ask questions about specific documents
- **Real-time Analysis:** Instant results with detailed explanations
- **Privacy Rights Guidance:** GDPR, CCPA, and consumer protection
- **Document Analysis:** Comprehensive legal document parsing and analysis
=======
### 📊 **Smart Analysis**
- **Automated Risk Detection**: Identifies unfair clauses using advanced pattern matching
- **Fairness Scoring**: 0-100 score based on legal best practices and consumer protection standards
- **Real-time Analysis**: Instant results with detailed explanations and context
- **Multi-Document Support**: Analyze Terms of Service, Privacy Policies, and EULAs
>>>>>>> main

### 🤖 **AI-Powered Chatbot**
- **Interactive Legal Assistant**: Ask questions about specific documents
- **Context-Aware Responses**: AI understands document content and provides relevant answers
- **Multi-Agent System**: Specialized agents for research, legal analysis, and document generation
- **Real-time Chat**: Built-in chatbot interface for document-specific questions

<<<<<<< main
- **Frontend:** HTML/CSS/JavaScript
- **Backend:** Python HTTP Server
- **AI:** NVIDIA AI Endpoints (Llama 3.1 8B)
- **Pattern Matching:** Enhanced regex for legal clause detection
- **Document Processing:** PDF parsing and text extraction
=======
### 🛡️ **Compliance & Privacy**
- **GDPR Compliance**: Detects data protection and user rights clauses
- **CCPA Compliance**: California privacy rights validation
- **COPPA Compliance**: Children's privacy protection checking
- **Privacy Rights Guidance**: Understand your data rights and protections
>>>>>>> main

## 🛠️ Technology Stack

### **Backend & AI/ML**
- **Python 3.x** - Core programming language
- **LangChain** - AI/ML framework for building agents
- **LangGraph** - State management and workflow orchestration
- **NVIDIA AI Endpoints** - GPU-accelerated AI inference
- **OpenAI API** - Language model integration
- **Tavily** - Web search and research capabilities
- **Pydantic** - Data validation and settings management

### **Web Server**
- **Python Built-in HTTP Server** - Custom server using `http.server.SimpleHTTPRequestHandler`
- **AsyncIO** - Asynchronous programming for AI agent calls
- **CORS Support** - Cross-origin resource sharing enabled

### **Frontend**
- **HTML5/CSS3** - Modern, responsive design with gradients
- **JavaScript (ES6+)** - Client-side logic and real-time analysis
- **Vanilla JS** - No framework dependencies

### **Document Processing**
- **PyPDF2** - PDF parsing and manipulation
- **PDFPlumber** - Advanced PDF text extraction

## ⚡ Quick Start

<<<<<<< main
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
=======
### 1. **Clone the Repository**
```bash
git clone https://github.com/Samanyu-Singh/nvidiaagentai.git
cd nvidiaagentai
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure API Keys** (Optional for enhanced AI features)
```bash
cp secrets.env.example secrets.env
# Edit secrets.env with your API keys:
# - NVIDIA_API_KEY
# - TAVILY_API_KEY
# - GITHUB_TOKEN
```

### 4. **Run the Web Server**
```bash
python server.py
```

### 5. **Open in Browser**
```
http://localhost:8000
```
>>>>>>> main

## 📊 How the Fairness Score Works

### **Base Score**: 100 points

### **Risk Deductions** (Points subtracted for problematic clauses):
- **Data Selling**: -40 (major violation of trust)
- **Extensive Data Sharing**: -35 (major privacy concern)
- **Broad Data Use**: -20 (AI training, advertising)
- **Lack of User Control**: -25 (no user agency)
- **Broad Liability Waivers**: -15 (extensive disclaimers)
- **Indefinite Data Retention**: -12 (privacy concern)
- **Waiver of Rights**: -12 (removes user rights)
- **Broad Termination Rights**: -8 (unfair termination)
- **Unilateral Changes**: -10 (common practice)
- **Mandatory Arbitration**: -8 (common practice)
- **Sole Discretion Clauses**: -6 (vague standards)
- **Excessive Data Collection**: -10 (privacy violations)
- **Automatic Renewal**: -4 (subscription practice)
- **No Refunds**: -3 (minor issue)

### **Compliance Bonuses** (Points added for good practices):
- **Fair Terms**: +15 (transparent practices)
- **Privacy Best Practices**: +15 (privacy-first approach)
- **GDPR**: +12 (important privacy protection)
- **CCPA**: +10 (consumer rights)
- **COPPA**: +10 (child protection)

### **Score Ranges**:
- **80-100**: ✅ **FAIR** - Good practices, user-friendly
- **60-79**: ⚠️ **MODERATE** - Some concerns but acceptable
- **0-59**: 🚨 **UNFAIR** - Significant issues, avoid if possible

## 🎯 Use Cases

### **Consumer Protection**
- Understand Terms of Service before agreeing
- Identify hidden data collection practices
- Spot unfair arbitration clauses
- Check refund and cancellation policies

### **Privacy Analysis**
- Verify data collection and sharing practices
- Check compliance with privacy regulations
- Understand your data rights
- Identify tracking and surveillance practices

### **Legal Education**
- Learn about your rights and unfair practices
- Understand legal terminology in plain English
- Compare different service agreements
- Make informed decisions about online services

### **Business Applications**
- Review vendor contracts and agreements
- Ensure compliance with privacy regulations
- Assess legal risks in partnerships
- Standardize contract review processes

## 🔍 How It Works

### **Risk Detection Patterns**
The system scans for problematic clauses like:
- **Data Selling**: "sell personal information", "share data with third parties"
- **Arbitration**: "binding arbitration", "waive jury trial"
- **Account Termination**: "terminate without notice", "suspend account"
- **Unfair Terms**: "no refunds", "waive all rights"
- **Privacy Violations**: "track across websites", "collect location data"
- **AI Training**: "machine learning models", "artificial intelligence training"

### **Compliance Validation**
Checks against major privacy frameworks:
- **GDPR**: "right to deletion", "data portability", "explicit consent"
- **CCPA**: "California privacy", "opt out of sale", "right to know"
- **COPPA**: "children under 13", "parental consent", "age verification"

### **AI-Powered Analysis**
- **Multi-Agent System**: Specialized agents for different analysis tasks
- **Context Understanding**: AI comprehends document meaning and implications
- **Intelligent Recommendations**: Actionable advice for document improvement
- **Interactive Chat**: Ask specific questions about document clauses

## 🏗️ Architecture

### **Multi-Agent System**
- **Researcher Agent**: Web research and legal precedent analysis
- **Legal Agent**: Document analysis and risk assessment
- **Author Agent**: Document generation and recommendations
- **Risk Analyzer**: Pattern matching and scoring algorithms

### **Web Interface**
- **Real-time Analysis**: Instant pattern matching and scoring
- **Interactive Chatbot**: AI-powered legal assistant
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Professional gradients and smooth animations

## 📁 Project Structure

```
nvidiaagentai/
├── server.py                 # Main web server
├── index.html               # Web interface
├── requirements.txt         # Python dependencies
├── secrets.env.example     # API key template
├── code/
│   └── docgen_agent/       # Core AI agents
│       ├── agent.py        # Base agent functionality
│       ├── legal_agent.py  # Legal analysis agent
│       ├── researcher.py   # Research agent
│       ├── author.py       # Document generation
│       ├── risk_analyzer.py # Risk detection & scoring
│       ├── tools.py        # Utility functions
│       └── models.py       # Data models
└── data/
    └── test_documents/     # Sample documents
```

## 🚀 Deployment

### **Local Development**
```bash
python server.py
```

### **Cloud Deployment**
The project is configured for GPU-accelerated cloud deployment on platforms like:
- **Brev Cloud** - NVIDIA GPU support
- **Google Colab** - Jupyter environment
- **AWS/GCP** - Scalable cloud deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

<<<<<<< main
- Built with NVIDIA's AI Endpoints
=======
- Built with **NVIDIA's AgentIQ Toolkit**
- Powered by **LangChain** and **LangGraph**
>>>>>>> main
- Inspired by consumer protection needs
- Designed for modern legal document analysis

---

**LegalLensIQ** - Making legal documents understandable, one clause at a time. 🔍⚖️


