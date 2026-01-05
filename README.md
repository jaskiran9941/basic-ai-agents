# 🤖 Basic AI Agents

A collection of foundational AI agent implementations, demonstrating the progression from simple to complex agentic systems.

## 📚 What's Inside

### 🎧 Agentic Podcast Summarizer
**Path:** `agentic-podcast-summarizer/`

An intelligent AI agent that autonomously manages podcast research and summarization.

**Why it's an agent:**
- ✅ Makes autonomous decisions (AI chooses what to do)
- ✅ Goal-oriented behavior (works toward objectives)
- ✅ Dynamic tool selection (picks tools based on context)
- ✅ Adaptive reasoning (changes strategy based on results)
- ✅ Context awareness (considers user preferences and state)

**Extension of:** [llm-apps/podcast-summarizer](../llm-apps/podcast-summarizer)

The original podcast-summarizer follows a fixed script. This agentic version lets the AI decide what to do based on goals and context.

---

## 🎯 Learning Path

This collection demonstrates **Option 1** from the agentic architecture spectrum:

```
Option 1              Option 2           Option 3           Option 4
Simple Agentic    →  Multi-Agent    →  MCP-Based      →  agnOS-Based
(This folder)        System             Agent              Enterprise

Complexity:  ★★☆☆☆      ★★★★☆            ★★★☆☆            ★★★★★
Use Case:    Learning    Specialized      Tool-rich        Production
                        roles            workflows         scale
```

---

## 🧠 What Makes Software "Agentic"?

### ❌ Not Agentic:
```python
# You write the control flow
def main():
    data = fetch()      # Always same
    result = process()  # Fixed steps
    send(result)        # No decision
```
**You decide** what happens

### ✅ Agentic:
```python
# AI writes the control flow
def main():
    agent = AIAgent(goal="Help user")
    agent.run()  # AI decides what to do
```
**AI decides** what happens

---

## 🚀 Quick Start

```bash
cd basic-ai-agents/agentic-podcast-summarizer
pip install -r requirements.txt
export ANTHROPIC_API_KEY='your-key'
python agentic_agent.py
```

---

## 📖 Key Concepts

### 1. Autonomous Decision-Making
The AI chooses actions based on context, not fixed logic.

### 2. Goal-Oriented Behavior
Works toward objectives, not just executing steps.

### 3. Dynamic Tool Use
Selects appropriate tools based on situation.

### 4. Adaptive Reasoning
Changes strategy based on results.

### 5. Context Awareness
Considers user state, preferences, environment.

---

## 🎓 Projects in This Collection

### Current:
- ✅ **Agentic Podcast Summarizer** - Simple agentic upgrade (Option 1)

### Coming Soon:
- 🔜 **Multi-Agent Research System** - Specialized agents working together (Option 2)
- 🔜 **MCP-Based Agent** - Standardized tool integration (Option 3)
- 🔜 **More basic agents** - Different domains and use cases

---

## 🔍 How to Use This Collection

### For Learning:
1. Start with **agentic-podcast-summarizer** to understand basics
2. Compare with non-agentic version in `llm-apps/podcast-summarizer`
3. Study how AI makes decisions vs hardcoded logic

### For Building:
1. Use as templates for your own agents
2. Understand tool calling patterns
3. Learn agentic loop architecture

### For Experimentation:
1. Modify prompts to change agent behavior
2. Add new tools and see how agent uses them
3. Test different scenarios

---

## 💡 Real-World Applications

These patterns apply to:
- **Research Assistants** - Autonomous information gathering
- **Content Curators** - Intelligent filtering and summarization
- **Personal Assistants** - Context-aware task management
- **Data Analysts** - Adaptive query and analysis
- **Customer Support** - Intelligent triage and routing

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **AI Brain** | Claude Sonnet 4 (Anthropic) |
| **SDK** | Anthropic SDK (native tool calling) |
| **Architecture** | Agentic loop with tool calling |
| **Language** | Python 3.8+ |

**Philosophy:** Minimal dependencies, maximum learning.
- ❌ No LangChain (using native SDK)
- ❌ No complex frameworks
- ✅ Clean, readable code
- ✅ Extensive comments and documentation

---

## 📚 Further Reading

- [What Are AI Agents? (Anthropic)](https://www.anthropic.com/research/ai-agents)
- [Tool Use Guide (Anthropic)](https://docs.anthropic.com/claude/docs/tool-use)
- [Building Autonomous Agents](https://www.anthropic.com/research/autonomous-agents)

---

## 🤝 Contributing

This is an educational collection. Feel free to:
- Add more basic agent examples
- Improve documentation
- Share your learnings
- Build on these patterns

---

## 📝 License

MIT License - Learn freely!

---

**Start your agent journey with `agentic-podcast-summarizer/`** 🤖
