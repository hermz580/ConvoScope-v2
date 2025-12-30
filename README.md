# ConvoScope 🔍

**Privacy-first conversation analytics for Claude AI**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

ConvoScope is a comprehensive toolkit for analyzing Claude AI conversations with deep insights into quality, patterns, and evolution - all while keeping your data private and processed locally.

**🌟 NOW WITH WEB INTERFACE!** ConvoScope v2.0 includes a modern, beautiful web application that makes conversation analysis accessible to everyone - no command line required!

![ConvoScope Banner](docs/assets/banner.png)

## ✨ Features

### 🌐 Modern Web Interface (NEW!)
- **Drag-and-drop** file upload
- **Real-time** progress tracking with WebSockets
- **Interactive** dashboards and visualizations
- **Beautiful** modern UI with Tailwind CSS
- **Responsive** design (works on desktop, tablet, mobile)
- **Zero installation** - just run and open in browser

### 🔒 Privacy-First Architecture
- **Automatic PII Redaction**: Removes emails, phone numbers, SSNs, credit cards, addresses, API keys
- **Entity Hashing**: Consistently anonymizes names while preserving analytical patterns
- **100% Local Processing**: Your data never leaves your machine
- **Configurable Protection**: Toggle privacy features based on your needs

### 📊 Deep Analytics
- **Conversation Quality Metrics**: Task completion tracking, collaboration scoring, response effectiveness
- **Temporal Evolution Analysis**: Track patterns over time, detect trend shifts, identify activity streaks
- **Advanced Failure Detection**: 11 failure types with severity levels (high/medium/low)
- **Topic Categorization**: 13+ categories with multi-topic support and custom patterns

### 📈 Rich Visualizations
- Topic distribution charts
- Sentiment trend analysis
- Activity heatmaps (day × hour)
- Failure type breakdowns
- Conversation length distributions
- Message evolution tracking
- Interactive HTML dashboards

### 📁 Multiple Output Formats
- Enhanced CSV with 25+ analytical columns
- Excel workbooks with 5 specialized analysis sheets
- Executive summaries with key insights
- Quality analysis reports
- Temporal evolution reports
- Publication-ready visualizations

## 🚀 Quick Start

### Two Ways to Use ConvoScope

#### Option 1: Web App (Recommended) ⭐

**The easiest and most beautiful way to use ConvoScope!**

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies (one-time setup)
cd frontend
npm install
cd ..

# 3. Start the backend server
python backend/app.py

# 4. In a new terminal, start the frontend
cd frontend
npm run dev

# 5. Open http://localhost:3000 in your browser
# 6. Drag and drop your Claude export JSON file
# 7. Watch the magic happen! ✨
```

#### Option 2: Command Line (Classic)

```bash
# Install dependencies
pip install -r requirements.txt

# Get your data from Claude.ai (Settings → Privacy → Download my data)

# Run analysis
python src/advanced_analyzer.py your_export.json

# With custom output name
python src/advanced_analyzer.py your_export.json my_analysis

# Skip visualizations for faster processing
python src/advanced_analyzer.py your_export.json output --no-viz
```

### Get Your Data

1. Go to [Claude.ai](https://claude.ai) → Settings → Privacy → "Download my data"
2. Wait for email with your data export (typically 1-3 days)
3. Extract the JSON file
4. Upload to ConvoScope web app or use with CLI

## 📖 Documentation

### User Guides
- [User Experience Walkthrough](docs/USER_EXPERIENCE_WALKTHROUGH.md) - See what the web app looks like
- [UX Improvement Plan](docs/UX_IMPROVEMENT_PLAN.md) - Our vision for the best UX
- [Usage Examples](docs/USAGE.md) - CLI usage guide
- [Privacy & Security](docs/PRIVACY.md)
- [Contributing](CONTRIBUTING.md)

### Technical Documentation
- [Frontend Architecture](docs/architecture/FRONTEND_ARCHITECTURE.md)
- [Backend Architecture](docs/architecture/BACKEND_ARCHITECTURE.md)
- [Frontend README](frontend/README.md)

### Development
- [Contributing Guidelines](CONTRIBUTING.md)

## 🎯 What Gets Analyzed

### Conversation Quality
- **Task Completion**: completed, in_progress, abandoned, blocked
- **Collaboration Quality**: high, medium, low, confrontational
- **Response Effectiveness**: highly_effective, effective, partially_effective, ineffective
- **Flow Patterns**: interruptions, timing gaps, response speed

### Topics (13 Categories)
- Technical/Coding (Python, APIs, debugging)
- AI/ML (models, training, LLMs)
- Custom Projects (BlaqVox, GrandRYZE, etc.)
- Healthcare/VA (medical, advocacy)
- Philosophy/Consciousness (Ubuntu, liberation frameworks)
- Creative/Art (music, design, generation)
- Personal/Life (relationships, advice)
- Infrastructure (Docker, deployment)
- Data Analysis (statistics, visualization)
- Documentation (technical writing)
- Debugging (troubleshooting)
- Security/Privacy (encryption, compliance)

### Sentiment Analysis (8 Levels)
- Very Positive / Positive
- Neutral
- Negative / Very Negative
- Urgent
- Questioning
- Collaborative

### Model Failures (11 Types)
**High Severity:**
- Hallucination (fabricated facts)
- Tool Misuse (incorrect tool selection)
- Context Loss (forgot previous conversation)
- Accuracy Error (factually wrong)
- Ignored Instructions (didn't follow directions)

**Medium Severity:**
- Unnecessary Refusal
- Repetition
- Misunderstanding
- Incomplete Response

**Low Severity:**
- Formatting Issues
- Performance Theater (excessive formality)

## 📊 Example Outputs

### Executive Summary
```
======================================================================
EXECUTIVE SUMMARY - CLAUDE CONVERSATION ANALYSIS
======================================================================

KEY METRICS:
--------------------------------------------------
Total Conversations: 847
Total Messages: 12,394
User Messages: 6,197
Assistant Messages: 6,197
Average Message Length: 412 characters
Average Words per Message: 67.3

TOP TOPICS:
--------------------------------------------------
Technical/Coding: 3,241
AI/ML: 2,156
Documentation: 1,893
...

SENTIMENT OVERVIEW:
--------------------------------------------------
Positive: 5,234 (42.2%)
Neutral: 4,891 (39.5%)
Urgent: 1,203 (9.7%)
...

MODEL PERFORMANCE:
--------------------------------------------------
Messages with Failures: 487
Failure Rate: 7.9%
```

### Quality Report
```
COLLABORATION QUALITY DISTRIBUTION:
--------------------------------------------------
high: 623 conversations (73.6%)
medium: 201 conversations (23.7%)
low: 23 conversations (2.7%)

TASK COMPLETION RATES:
--------------------------------------------------
completed: 712 conversations (84.1%)
in_progress: 98 conversations (11.6%)
abandoned: 37 conversations (4.4%)
```

## 🛠️ Advanced Usage

### Custom Analysis

```python
from src.advanced_analyzer import AdvancedConversationAnalyzer

# Initialize with options
analyzer = AdvancedConversationAnalyzer(
    'export.json',
    enable_privacy=True,
    enable_quality_analysis=True,
    enable_temporal_analysis=True,
    enable_visualizations=False
)

# Run analysis
analyzer.load_data()
analyzer.parse_conversations_advanced()

# Access dataframe for custom analysis
df = analyzer.df
tech_conversations = df[df['topics'].str.contains('Technical')]
```

### Integration with Other Tools

```python
import pandas as pd

# Load the CSV
df = pd.read_csv('analysis.csv')

# Filter high-quality technical conversations
high_quality_tech = df[
    (df['topics'].str.contains('Technical')) &
    (df['collaboration_quality'] == 'high') &
    (df['has_failure'] == False)
]

# Export to database
from sqlalchemy import create_engine
engine = create_engine('postgresql://localhost/convoscope')
df.to_sql('conversations', engine, if_exists='replace')
```

## 🏗️ Architecture

ConvoScope uses a modular architecture for extensibility and maintainability:

```
src/
├── advanced_analyzer.py      # Main orchestrator
├── quality_analyzer.py        # Quality metrics module
├── temporal_analyzer.py       # Time-based analysis
├── visualization_generator.py # Charts and graphs
└── claude_conversation_analyzer.py # Base analyzer
```

Each module can be used independently or as part of the comprehensive analysis pipeline.

## 🔐 Privacy & Security

### What Gets Redacted
- Email addresses
- Phone numbers  
- Social Security Numbers
- Credit card numbers
- Physical addresses
- IP addresses
- API keys and tokens

### What Gets Hashed
- Person names (consistently hashed for pattern preservation)
- Organizations (when configured)

### Local-Only Processing
All analysis runs on your local machine. No data is transmitted to external servers, no cloud processing, no third-party analytics. Your conversation data stays under your control.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/convoscope.git
cd convoscope

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built for liberation infrastructure work - creating tools that serve community empowerment rather than corporate extraction.

Inspired by Ubuntu philosophy: "I am because we are."

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/convoscope/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/convoscope/discussions)
- **Documentation**: [Full Docs](docs/)

## 🗺️ Roadmap

### ✅ Completed (v2.0)
- [x] Interactive web dashboard with React + Flask
- [x] Real-time progress tracking with WebSockets
- [x] Modern, beautiful UI with Tailwind CSS
- [x] Drag-and-drop file upload
- [x] Comprehensive architecture documentation

### 🚧 In Progress
- [ ] Complete dashboard UI implementation
- [ ] Interactive visualizations with drill-down
- [ ] Conversation browser and search
- [ ] Privacy dashboard with network monitor
- [ ] Smart insights engine

### 📋 Planned
- [ ] Vector database export for semantic search
- [ ] LLM-powered insight generation
- [ ] Conversation similarity clustering
- [ ] Multi-user comparison analysis
- [ ] Progressive Web App (PWA) support
- [ ] Export connectors for BI tools
- [ ] Plugin system for custom analyzers

## ⭐ Star History

If you find ConvoScope useful, please consider starring the repository!

---

**Remember**: ConvoScope processes all data locally. Your conversations never leave your machine unless you choose to share the outputs.
