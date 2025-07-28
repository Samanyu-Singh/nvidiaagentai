# LegalLensIQ Web Interface

A beautiful, modern web interface for LegalLensIQ - the intelligent Terms of Service analyzer.

## 🚀 Quick Start

### Option 1: Run the Web Server
```bash
python3 server.py
```
This will:
- Start a web server on port 8000
- Automatically open your browser
- Load the LegalLensIQ interface

### Option 2: Open Directly in Browser
Simply open `index.html` in any modern web browser.

## 🌟 Features

### 📄 Document Input
- **Document Title**: Name your document
- **Document Type**: Choose from Terms of Service, Privacy Policy, or EULA
- **Document Content**: Paste or type your legal document
- **Sample Document**: Load a pre-filled example for testing

### 📊 Analysis Results
- **Fairness Score**: 0-100 rating with color-coded status
- **Risk Analysis**: Detects problematic clauses
- **Compliance Check**: Validates against GDPR, COPPA, CCPA
- **Smart Recommendations**: Actionable advice for improvement

### 🎨 Modern UI
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful Gradients**: Professional purple gradient background
- **Smooth Animations**: Loading spinners and hover effects
- **Color-Coded Results**: Green for good, yellow for warnings, red for risks

## 🔍 How It Works

### Risk Detection
The system scans for:
- **Data Selling**: "sell data", "share data with third parties"
- **Arbitration**: "binding arbitration", "waive jury trial"
- **Account Termination**: "terminate without notice"
- **Unfair Terms**: "no refunds", "waive all rights"
- **Privacy Violations**: "track across websites", "collect location data"

### Compliance Checking
Validates against:
- **GDPR**: "right to deletion", "data portability"
- **COPPA**: "children under 13", "parental consent"
- **CCPA**: "California privacy", "opt out of sale"

### Fairness Scoring
- **Base Score**: 100 points
- **Risk Deductions**: -20 for data selling, -15 for arbitration, etc.
- **Compliance Bonuses**: +10 for GDPR, +5 for CCPA, etc.
- **Final Score**: 0-100 with clear status indicators

## 🎯 Perfect for Hackathons

### Professional Presentation
- **Modern Design**: Looks professional and polished
- **Interactive Demo**: Judges can try it themselves
- **Clear Results**: Easy to understand analysis
- **Mobile Friendly**: Works on any device

### Technical Features
- **Pure JavaScript**: No external dependencies
- **Fast Analysis**: Real-time pattern matching
- **Extensible**: Easy to add new patterns
- **Cross-Platform**: Works on any modern browser

## 📱 Usage

1. **Load the Interface**: Run `python3 server.py` or open `index.html`
2. **Enter Document**: Paste your Terms of Service or use the sample
3. **Click Analyze**: Watch the loading animation
4. **Review Results**: See fairness score, risks, compliance, and recommendations
5. **Try Different Documents**: Test with various legal texts

## 🛠️ Customization

### Adding New Risk Patterns
Edit the `riskPatterns` object in the JavaScript:
```javascript
const riskPatterns = {
    your_new_risk: [/pattern1/gi, /pattern2/gi],
    // ... existing patterns
};
```

### Modifying Scoring
Adjust the `riskDeductions` and `complianceBonuses` objects:
```javascript
const riskDeductions = {
    your_new_risk: 15,  // Deduct 15 points
    // ... existing deductions
};
```

## 🎉 Ready for Your Hackathon!

Your LegalLensIQ web interface is:
- ✅ **Professional looking**
- ✅ **Fully functional**
- ✅ **Easy to demonstrate**
- ✅ **Impressive to judges**
- ✅ **Ready to present**

**Start the server and show off your intelligent legal document analyzer!** 