# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
cd basic-ai-agents/agentic-podcast-summarizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### 3. Run the Agent

```bash
# Run demonstration
python agentic_agent.py

# Or run examples
python examples.py
```

---

## 🎯 Why This Is Different

### Traditional (Non-Agentic)
```python
# You write the logic
episodes = fetch_all()
for ep in episodes:
    summarize(ep)
send_email()
```

### Agentic (This Project)
```python
# AI writes the logic
agent = AgenticAgent()
agent.run("Get me valuable insights")
# AI decides: what to fetch, what to summarize, what to send
```

---

## 💡 Try These Commands

```python
from agentic_agent import AgenticPodcastSummarizer

agent = AgenticPodcastSummarizer()

# Example 1: Busy user
agent.run_agentic_workflow(
    "I'm busy, only important AI news, keep it brief"
)

# Example 2: Deep dive
agent.run_agentic_workflow(
    "Find me content about AI safety, I have time for details"
)

# Example 3: Discovery
agent.run_agentic_workflow(
    "Suggest new podcasts about quantum computing"
)
```

---

## 🔍 Watch the Agent Think

When you run the agent, you'll see:

```
💭 AI Reasoning:
"User is busy, so I should check preferences first to understand
what's important to them, then filter aggressively..."

🔧 Executing tool: check_user_preferences
   Result: {interests: ['AI', 'technology'], preferred_length: 'brief'}

💭 AI Reasoning:
"User likes AI topics and wants brief summaries. Let me fetch episodes
and filter for high-relevance AI content only..."

🔧 Executing tool: fetch_new_episodes
   Input: {hours_back: 24}
   Result: 3 episodes found

💭 AI Reasoning:
"Episode 1 is about AI (high relevance), Episode 2 is about cooking
(skip), Episode 3 is about NVIDIA chips (relevant). I'll process
episodes 1 and 3 with brief summaries..."
```

This is **autonomous decision-making** in action!

---

## 📊 What Makes It Agentic?

| Feature | Traditional | Agentic (This) |
|---------|-------------|----------------|
| **Who decides what to do?** | You (programmer) | AI (Claude) |
| **Adapts to context?** | No | Yes |
| **Filters intelligently?** | No | Yes |
| **Chooses summary style?** | Fixed | Dynamic |

---

## 🎓 Next Steps

1. **Understand the code**: Read `agentic_agent.py` comments
2. **Run examples**: Execute `examples.py` for scenarios
3. **Read README**: Full explanation of agentic behavior
4. **Experiment**: Modify prompts and see how agent adapts

---

## 🆘 Troubleshooting

**Error: "ANTHROPIC_API_KEY not found"**
- Set environment variable: `export ANTHROPIC_API_KEY='your-key'`
- Or create `.env` file with your key

**Want to connect to real podcasts?**
- Uncomment dependencies in `requirements.txt`
- Import actual modules from `llm-apps/podcast-summarizer`
- Replace mock data in `execute_tool()` method

---

**Ready to see an agent in action? Run `python agentic_agent.py` now!** 🤖
