# 🤖 AI Content Discovery Agent - Starter Project

A production-ready AI agent that intelligently discovers and curates resources across 6 different sources. Perfect for learning how to build, deploy, and optimize AI agents.

**Live Demo:** Search any topic and get curated recommendations from web articles, GitHub repos, books, YouTube videos, Reddit discussions, and academic papers.

![Agent Architecture](https://img.shields.io/badge/Agent-Multi--Tool-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-green) ![Anthropic](https://img.shields.io/badge/LLM-Claude-purple) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 What Makes This a Real Agent?

This isn't just a script that calls APIs - it's a true AI agent with:

- **Autonomous Decision-Making**: The agent decides which sources to search based on your topic
- **Dynamic Tool Selection**: Uses GitHub for technical topics, skips it for lifestyle topics
- **Quality Filtering**: Filters out irrelevant results before presenting them
- **Intelligent Synthesis**: Combines and ranks results from multiple sources
- **Adaptive Behavior**: Adjusts strategy based on topic type and available tools

### Example: Agent Reasoning

**Topic:** "React hooks tutorial"
- Agent thinks: *"This is a technical topic, I should search code repos, videos, and articles"*
- Uses: Web Search + GitHub + YouTube + Books
- Skips: Reddit, arXiv (not relevant)

**Topic:** "being a better partner"
- Agent thinks: *"This is a lifestyle topic, no code needed"*
- Uses: Web Search + Books + YouTube + Reddit
- Skips: GitHub, arXiv (not relevant)

---

## 🚀 Features

### ✅ 6 Data Sources (All Free/Freemium)
- 🌐 **Web Search** (Tavily API) - Articles and blogs
- 💻 **GitHub** - Code repositories and projects
- 📚 **Google Books** - Books and publications
- 🎥 **YouTube** - Video tutorials and talks
- 💬 **Reddit** - Community discussions
- 📄 **arXiv** - Academic papers and research

### ✅ Quality Controls
- Result filtering for relevance
- Duplicate removal
- Quality ranking
- Error handling and fallbacks

### ✅ Modern Web UI
- Clean, professional interface
- Clickable results with metadata
- Real-time search
- Cost tracking per query

### ✅ Production-Ready Patterns
- Proper error handling
- API rate limiting
- Configurable tools
- Extensible architecture

---

## 🎯 Who This Is For

- **Product Managers** learning about AI agents
- **Developers** building their first agent
- **Students** studying LLM applications
- **Researchers** exploring multi-tool agents
- **Anyone** wanting to understand how AI agents work

---

## 📋 Prerequisites

- Python 3.8 or higher
- API keys (all have free tiers):
  - Anthropic (Claude)
  - Tavily Search
  - GitHub
  - Google Cloud (for Books & YouTube)

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-content-discovery-agent.git
cd ai-content-discovery-agent
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get API Keys

#### Anthropic (Claude) - Required
1. Go to https://console.anthropic.com/
2. Sign up and get API key
3. **Cost:** $5 free credit, then ~$0.02 per query

#### Tavily Search - Required
1. Go to https://tavily.com/
2. Sign up for free tier
3. **Cost:** 1000 searches free/month

#### GitHub Token - Required
1. Go to https://github.com/settings/tokens
2. Generate token with `public_repo` scope
3. **Cost:** Free

#### Google Cloud (Books & YouTube) - Required
1. Go to https://console.cloud.google.com/
2. Create project
3. Enable "Google Books API" and "YouTube Data API v3"
4. Create API key
5. **Cost:** Free (Books: 1000/day, YouTube: quota limits)

### 5. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
ANTHROPIC_API_KEY=your_anthropic_key_here
TAVILY_API_KEY=your_tavily_key_here
GITHUB_TOKEN=your_github_token_here
GOOGLE_BOOKS_API_KEY=your_google_key_here
```

### 6. Run the Application

```bash
streamlit run app.py
```

Open your browser to: http://localhost:8501

---

## 🎮 Usage

### Web Interface

1. **Enter a topic** in the search box
2. **Click "Discover"** to search
3. **View results** organized by source
4. **Click any title** to visit the source

### Quick Examples (in sidebar)

- **Technical:** React hooks tutorial, Python machine learning
- **Learning:** AI Product Management, Data science career
- **Lifestyle:** Being a better partner, Meditation for beginners

### Command Line

```python
from agent import ContentDiscoveryAgent

agent = ContentDiscoveryAgent()
result = agent.discover("AI Product Management")
print(result['results'])
```

---

## 📁 Project Structure

```
ai-content-discovery-agent/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
│
├── app.py                   # Streamlit web interface
├── agent.py                 # Main agent orchestration
├── config.py                # Configuration management
│
├── tools/                   # Tool implementations
│   ├── __init__.py
│   ├── web_search.py       # Tavily web search
│   ├── github_search.py    # GitHub repository search
│   ├── books_search.py     # Google Books search
│   ├── youtube_search.py   # YouTube video search
│   ├── reddit_search.py    # Reddit discussions
│   └── arxiv_search.py     # arXiv papers
│
├── examples/               # Example scripts
│   └── test_agent.py      # Test different topics
│
└── docs/                   # Documentation
    ├── SETUP_GUIDE.md     # Detailed setup
    ├── LEARNING_NOTES.md  # Learning guide
    └── QUICK_START.md     # Quick start guide
```

---

## 🧠 Architecture

### Agent Flow

```
User Input
    ↓
Claude (LLM) with Tools
    ↓
[Reasoning Loop]
    ↓
Tool Selection → Tool Execution → Result Processing
    ↓                ↓                  ↓
web_search      API Call          Back to Agent
github_search   API Call          Back to Agent
books_search    API Call          Back to Agent
youtube_search  API Call          Back to Agent
reddit_search   API Call          Back to Agent
arxiv_search    API Call          Back to Agent
    ↓
[End Loop]
    ↓
Synthesis & Quality Filtering
    ↓
Structured Output
```

### Key Components

1. **Agent Orchestrator** (`agent.py`)
   - Manages conversation with Claude
   - Handles tool calling loop
   - Tracks costs and tokens

2. **Tool Layer** (`tools/`)
   - Each tool is independent
   - Standardized input/output
   - Error handling per tool

3. **Quality Layer** (`tools/books_search.py`)
   - Result filtering
   - Relevance checking
   - Deduplication

4. **UI Layer** (`app.py`)
   - Clean interface
   - Real-time updates
   - Result visualization

---

## 💰 Cost Breakdown

**Per Query (Average):**
- Anthropic (Claude): $0.01-0.03
- Tavily: $0.001
- Other APIs: Free

**Total: ~$0.02 per search**

**For Testing:**
- 50 searches: ~$1.00
- 500 searches: ~$10.00

---

## 🎓 Learning Resources

### For Product Managers
- `docs/LEARNING_NOTES.md` - Understand agent concepts
- Study tool selection logic in `agent.py`
- Compare with/without quality filtering

### For Developers
- `tools/` directory - See how to integrate APIs
- `agent.py` - Learn the ReAct pattern
- `examples/test_agent.py` - Test different scenarios

### Key Concepts Taught
1. **Agent vs Script** - Autonomous decision-making
2. **Tool Calling** - How LLMs use external APIs
3. **ReAct Pattern** - Reasoning + Acting loop
4. **Quality Control** - Filtering and ranking
5. **Cost Optimization** - Managing token usage
6. **Error Handling** - Graceful degradation

---

## 🔨 Customization

### Add a New Tool

1. Create `tools/your_tool.py`:

```python
def your_search(query: str, max_results: int = 5):
    # Your API call here
    return {
        "success": True,
        "results": [...],
        "total": len(results)
    }

YOUR_TOOL = {
    "name": "your_search",
    "description": "...",
    "input_schema": {...}
}
```

2. Add to `agent.py`:

```python
from tools.your_tool import your_search, YOUR_TOOL

self.tools.append(YOUR_TOOL)
self.tool_functions["your_search"] = your_search
```

### Modify Agent Behavior

Edit the system prompt in `agent.py` (line 93) to change how the agent thinks about tool selection.

---

## 🐛 Troubleshooting

### "Missing API keys"
- Check your `.env` file exists
- Verify all keys are set
- No quotes around keys

### "YouTube API error"
- Enable "YouTube Data API v3" in Google Cloud Console
- Wait 30 seconds after enabling
- Verify API key has access

### "No results from Reddit"
- Reddit's search API can be flaky
- Try a different query
- Check User-Agent header in `tools/reddit_search.py`

### "Poor quality results"
- Check `tools/books_search.py` filtering logic
- Adjust relevance thresholds
- Add more filters

---

## 🚀 Next Steps

### Beginner
1. Run the agent with different topics
2. Observe which tools get selected
3. Read `docs/LEARNING_NOTES.md`

### Intermediate
1. Add a new tool (podcasts, Twitter, etc.)
2. Improve quality filtering
3. Implement caching

### Advanced
1. Add parallel tool execution
2. Implement result ranking with ML
3. Build multi-agent collaboration
4. Add memory and context

---

## 📚 Related Projects

- [LangChain](https://github.com/langchain-ai/langchain) - Full agent framework
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Autonomous agents
- [Composio](https://github.com/ComposioHQ/composio) - Tool integration platform

---

## 🤝 Contributing

Contributions welcome! Areas to improve:

- [ ] Add more data sources (podcasts, Twitter/X, Medium)
- [ ] Implement caching layer
- [ ] Add result ranking algorithm
- [ ] Parallel tool execution
- [ ] Better error recovery
- [ ] Unit tests
- [ ] Docker support

---

## 📄 License

MIT License - feel free to use this for learning or commercial projects.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude API and excellent tool use capabilities
- **Tavily** for agent-optimized search API
- **Streamlit** for easy web interface development

---

## 📬 Contact

Questions? Issues? Suggestions?

- Open an issue on GitHub
- Star ⭐ this repo if you found it helpful
- Share your agent projects built with this starter!

---

## 🎯 Built for Learning

This project is specifically designed to teach:
- How real AI agents work (not just API wrappers)
- Production patterns for agent development
- Cost-effective development with free tiers
- Quality control in non-deterministic systems

**Perfect for your first agent project or portfolio piece!**

---

**⭐ Star this repo if you found it useful!**

**🔗 Share your projects built with this starter!**
