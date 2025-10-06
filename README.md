# 🎯 JobMatch AI

An intelligent **agent-based** tool to find jobs that match your profile using NLP and embeddings.

## 🚀 Features

- 🤖 **Agent Architecture** - Modular tool-based system for flexibility
- 📄 **Multi-format Input** - PDF, JSON, or manual profile entry
- 🔍 **Real-time Job Search** - Powered by Adzuna API
- 🎯 **Smart Matching** - Embeddings + cosine similarity for accurate matches
- 🌍 **Multi-country Support** - Germany, UK, Netherlands, and more
- 🔧 **CLI Interface** - Simple command-line usage

## 🏗️ Technologies Used

- **Python 3.12+**
- **LangChain** - Agent framework and tool calling
- **Hugging Face** - Sentence embeddings (all-MiniLM-L6-v2)
- **spaCy** - Text preprocessing and lemmatization
- **PyMuPDF** - PDF parsing
- **Adzuna API** - Job data retrieval
- **scikit-learn** - Cosine similarity

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  JobMatchAgent                          │
│              (Workflow Orchestrator)                    │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ProfileParser │   │ JobSearcher  │   │ JobFilter    │
│     Tool     │   │     Tool     │   │     Tool     │
└──────────────┘   └──────────────┘   └──────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │ JobMatcher   │
                   │     Tool     │
                   └──────────────┘
```

## 🔄 How It Works

1. **Profile Parsing** → Load profile from PDF/JSON
2. **Job Search** → Fetch relevant jobs from Adzuna
3. **Smart Filtering** → Filter by location, type, keywords
4. **AI Matching** → Match using embeddings and similarity

## 📦 Installation

### Prerequisites
- Python 3.12+
- Adzuna API credentials (free at [developer.adzuna.com](https://developer.adzuna.com/))

### Setup

```bash
# Clone repository
git clone https://github.com/ckakgun/jobmatch-ai.git
cd jobmatch-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Configuration

Create `.env` file in project root:
```env
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
```

## 🎯 Usage

### Option 1: Agent CLI (Recommended)

Basic usage:
```bash
python src/run_agent.py --pdf data/linkedin_profile.pdf
```

Custom search:
```bash
python src/run_agent.py \
  --pdf data/resume.pdf \
  --query "Machine Learning Engineer" \
  --location "London" \
  --top 5
```

With filtering:
```bash
python src/run_agent.py \
  --json data/profile.json \
  --query "AI engineer" \
  --countries de uk nl \
  --keywords pytorch tensorflow nlp
```

### Option 2: Python API

```python
from agents import JobMatchAgent

# Initialize agent
agent = JobMatchAgent()

# Run workflow
results = agent.run_workflow(
    profile_source="pdf",
    profile_path="data/linkedin_profile.pdf",
    job_query="AI engineer",
    job_location="Berlin",
    top_n=3
)

# Display results
agent.display_results(results)
```

### Option 3: Direct Tool Usage

```python
from agents import JobMatchAgent

agent = JobMatchAgent()

# List available tools
tools = agent.list_tools()

# Call specific tool
result = agent.call_tool('job_searcher', {
    "query": "AI engineer",
    "location": "Berlin"
})
```


## 📊 Example Output

```
🤖 Initializing JobMatch AI Agent...
📋 Profile: data/linkedin_profile.pdf
🔍 Query: AI engineer
📍 Location: Berlin
🎯 Top: 3

================================================================================
🔄 Step 1: Parsing profile...
✅ Profile loaded: Ceren Kaya Akgün

🔄 Step 2: Searching jobs for 'AI engineer' in Berlin...
✅ Found 50 jobs

🔄 Step 3: Filtering jobs...
✅ Filtered to 50 jobs (100.0%)

🔄 Step 4: Matching jobs to profile...
✅ Found 3 top matches

================================================================================
🎯 JOB MATCHING RESULTS
================================================================================

📊 Workflow Summary:
  • Profile: Ceren Kaya Akgün
  • Jobs Found: 50
  • Jobs Filtered: 50
  • Top Matches: 3

🔹 Top 3 Matches:
--------------------------------------------------------------------------------

#1. AI Software Engineer (all genders)
    🏢 Lingoda
    📍 Deutschland, DE
    🔗 https://www.adzuna.de/details/5348336248

#2. (Senior) AI Engineer (m/f/d)
    🏢 Simon-Kucher & Partners
    📍 Deutschland, DE
    🔗 https://www.adzuna.de/details/5415829667

#3. (Senior) Data Scientist / AI Engineer
    🏢 Cherry Ventures
    📍 Deutschland, DE
    🔗 https://www.adzuna.de/details/5414268205
```

## 🛠️ Project Structure

```
jobmatch-ai/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── job_match_agent.py      # Main agent orchestrator
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── profile_tool.py         # Profile parsing
│   │   ├── search_tool.py          # Job search
│   │   ├── filter_tool.py          # Job filtering
│   │   └── match_tool.py           # Job matching
│   ├── embedding_utils.py          # Embeddings
│   ├── text_preprocessing.py       # Text processing
│   ├── parse_profile.py            # Profile parsing
│   ├── job_search.py               # API integration
│   ├── match_jobs.py               # Matching logic
│   └── run_agent.py                # Agent CLI
├── data/
│   ├── linkedin_profile.pdf        # Your profile
│   ├── linkedin_profile.json       # Parsed profile
│   └── job_postings.json           # Fetched jobs
├── .env                            # API credentials
├── requirements.txt                # Dependencies
├── README.md                       # This file
└── AGENT_USAGE.md                  # Detailed agent docs
```

## 🔧 Advanced Usage

See [AGENT_USAGE.md](AGENT_USAGE.md) for:
- Detailed tool documentation
- Custom workflow creation
- Adding new tools
- API integration examples
- Extending the agent

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- [Adzuna](https://www.adzuna.com/) for job data API
- [LangChain](https://langchain.com/) for agent framework
- [Hugging Face](https://huggingface.co/) for embeddings
- [spaCy](https://spacy.io/) for NLP

## 📧 Contact

Created by [Ceren Akgun](https://github.com/ckakgun)

---

⭐ Star this repo if you find it useful!