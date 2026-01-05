# 🤖 Agentic Podcast Summarizer

**An intelligent, autonomous AI agent for podcast discovery and summarization powered by real data.**

> **This is an agentic enhancement of the [podcast-summarizer](https://github.com/jaskiran9941/llm-apps/tree/main/podcast-summarizer) project.**
>
> Instead of following a fixed script with hardcoded RSS feeds, this AI agent **autonomously decides** what to do based on your goals, searches real podcast databases, and adapts its behavior to context.

---

## 🎯 What Makes This REALLY Agentic?

### Key Difference from Original Project

| Aspect | [Original Podcast Summarizer](https://github.com/jaskiran9941/llm-apps/tree/main/podcast-summarizer) | **This Agentic Version** |
|--------|-------------|------------------------|
| **Data Source** | You provide exact RSS feed URLs | **Agent searches iTunes API dynamically** |
| **Control Flow** | Fixed: Fetch → Transcribe → Summarize | **AI decides** what to do and in what order |
| **Filtering** | Processes ALL episodes | **AI filters** based on your interests |
| **Summarization** | Same style every time | **AI adapts** style (brief/detailed/technical) |
| **Discovery** | You find podcasts manually | **AI searches** for new podcasts on topics you care about |
| **Decision Making** | Your hardcoded logic | **AI reasons** and makes autonomous choices |

### The Core Transformation

**Original (Non-Agentic):**
```python
# YOU decide everything
rss_feeds = ["https://lexfridman.com/feed/podcast/", ...]  # Hardcoded!

for feed in rss_feeds:
    episodes = fetch_episodes(feed)      # Process all
    for episode in episodes:              # Same steps every time
        transcript = get_transcript(episode)
        summary = summarize(transcript)  # Same style
    send_email(summaries)                 # Always send
```
**Decision maker:** Your hardcoded code

**This Agentic Version:**
```python
# AI decides everything
agent = AgenticAgent(
    goal="Get me valuable AI podcast insights from the last 24 hours"
)

# AI autonomously:
# - Checks your interests first
# - Searches iTunes API for new AI podcasts
# - Parses RSS feeds from subscriptions
# - Filters episodes by relevance
# - Chooses appropriate summary style
# - Decides whether to send or save for later

agent.run()  # Fully autonomous!
```
**Decision maker:** OpenAI GPT-4

---

## 🌐 Real Data Sources (Not Mock!)

This agent uses **100% real data**:

| Data Source | Purpose | API Used |
|-------------|---------|----------|
| **🍎 iTunes/Apple Podcasts** | Discover new podcasts | [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/) |
| **📡 RSS Feeds** | Fetch actual episodes | feedparser library |
| **🤖 OpenAI GPT-4** | Generate real summaries | OpenAI API |

**No mock data!** When you run this agent:
- It searches the **actual iTunes catalog** (millions of podcasts)
- It parses **real RSS feeds** from subscribed shows
- It generates **real AI summaries** using GPT-4

---

## 🧠 The 5 Characteristics of Agentic AI

This system demonstrates all 5 core characteristics that make it a **true AI agent**:

### 1. ✅ Autonomous Decision-Making
**AI chooses actions** based on context, not your hardcoded if/else logic.

**Example:**
```
User: "I'm extremely busy this week"

AI Reasoning:
→ User is busy → use 'brief' summary style
→ Only process high-relevance episodes (score > 0.8)
→ Skip lengthy technical deep dives
→ Only send if genuinely important
```

### 2. ✅ Goal-Oriented Behavior
**Works toward objectives**, not just executing predetermined steps.

**Example:**
```
Goal: "Find me content about AI safety"

AI's Plan:
1. Check user preferences to understand existing interests
2. Search iTunes API for "AI safety" podcasts
3. Check current subscriptions for safety-related episodes
4. If not enough content → search for more sources
5. Prioritize episodes specifically about safety, not general AI
```

### 3. ✅ Dynamic Tool Selection
**Selects tools** based on the situation, not in a fixed sequence.

**Example:**
```
Scenario A: User wants new podcast recommendations
→ AI: search_web_for_podcasts() → analyze_relevance() → generate_summary()

Scenario B: User wants updates from subscriptions
→ AI: check_user_preferences() → fetch_new_episodes() → generate_summary()

Same agent, different tool sequences!
```

### 4. ✅ Planning & Reasoning
**Thinks before acting** - you can see its reasoning process.

**Example from actual run:**
```
💭 AI Reasoning:
"Before fetching episodes, I should check the user's preferences to
understand what topics they're interested in. Then I'll fetch recent
episodes from their subscriptions and also search iTunes for new AI
podcasts they might not know about. Since they mentioned being busy,
I'll use brief summaries and only send if there's high-value content."
```

### 5. ✅ Adaptive Behavior
**Observes results** and adjusts strategy accordingly.

**Example:**
```
Iteration 1: fetch_new_episodes(24 hours) → finds 0 episodes
Iteration 2: AI observes → "No recent episodes in 24 hours"
Iteration 3: AI adapts → "I should search for older episodes or
              discover new podcasts instead of just failing"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         AI Agent (GPT-4 Turbo)                  │
│                                                 │
│  - Analyzes your goal                           │
│  - Reasons about best approach                  │
│  - Selects appropriate tools                    │
│  - Adapts based on results                      │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Dynamic Tool Selection
                   │
        ┌──────────┼────────────┬─────────────┐
        ▼          ▼            ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌──────────┐ ┌──────────────┐
│Search iTunes│ │Fetch Episodes│ │Analyze   │ │Generate      │
│API for      │ │from RSS      │ │Relevance │ │GPT-4 Summary │
│Podcasts     │ │Feeds         │ │Score     │ │              │
└─────────────┘ └─────────────┘ └──────────┘ └──────────────┘
     │               │              │              │
     │ REAL API      │ REAL RSS     │ AI Analysis  │ REAL GPT-4
     │               │              │              │
     └───────────────┴──────────────┴──────────────┘
```

**Key Components:**

1. **AI Orchestrator Layer** (NEW - The Agentic Part)
   - GPT-4 makes all decisions
   - Uses OpenAI tool calling API
   - Implements agentic loop (perceive → reason → act → adapt)

2. **Real Data Integration Layer** (NEW)
   - iTunes Search API for podcast discovery
   - feedparser for RSS parsing
   - OpenAI GPT-4 for summarization
   - No mock data!

3. **Tool Execution Layer** (NEW)
   - Maps AI's tool choices to actual API calls
   - Handles errors gracefully
   - Returns results back to AI for adaptation

4. **Streamlit Visualization** (NEW)
   - Watch AI think in real-time
   - See tool calls and results
   - Understand decision-making process

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/))

### Installation

```bash
# Clone the repo
git clone https://github.com/jaskiran9941/basic-ai-agents.git
cd basic-ai-agents/agentic-podcast-summarizer

# Install dependencies
pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Run the Agent

```bash
# Run with Streamlit UI (recommended)
streamlit run app_real.py

# The app will open at http://localhost:8502
```

---

## 💡 Usage Examples

### Example 1: Busy User (Context-Aware Filtering)

**Goal:** "I'm extremely busy this week. Only send me insights if there's something genuinely important about AI. Keep it brief."

**What the AI Agent Does:**
1. ✅ Calls `check_user_preferences()` to understand interests
2. ✅ Calls `fetch_new_episodes(24)` from subscriptions
3. ✅ Parses **real RSS feeds** (Lex Fridman, a16z, The AI Podcast)
4. ✅ Calls `analyze_episode_relevance()` for each episode
5. ✅ **Skips** cooking podcasts, sports content (low relevance)
6. ✅ Only processes AI-related episodes (high relevance)
7. ✅ Calls `generate_summary(style="brief")` - adapts to busy context
8. ✅ Only sends email if genuinely valuable content found

**Agent's Reasoning:**
```
💭 AI Reasoning:
"User is busy, so I need to be highly selective. I'll check their
preferences, fetch recent episodes, but ONLY summarize those with
relevance_score > 0.8. I'll use brief summaries to respect their time."
```

### Example 2: Discovery Mode (Proactive Search)

**Goal:** "I want to learn about AI safety. Find relevant content from my podcasts or suggest new ones."

**What the AI Agent Does:**
1. ✅ Calls `check_user_preferences()`
2. ✅ Calls `fetch_new_episodes()` - checks current subscriptions first
3. ✅ Finds limited AI safety content in subscriptions
4. ✅ **Proactively** calls `search_web_for_podcasts(topics=["AI safety"])`
5. ✅ **Real iTunes API search** returns new podcast recommendations
6. ✅ Analyzes episodes from both sources
7. ✅ Uses `detailed` summary style (user has learning goal, not rushed)
8. ✅ Provides recommendations for new podcasts to subscribe to

**Agent's Reasoning:**
```
💭 AI Reasoning:
"User wants to learn about AI safety. Current subscriptions might not
have enough content on this specific topic. I should search iTunes for
AI safety podcasts and provide recommendations."
```

### Example 3: Technical Deep Dive

**Goal:** "I have time this weekend for deep technical content about machine learning. Give me detailed summaries."

**What the AI Agent Does:**
1. ✅ Searches for machine learning content
2. ✅ Filters for technical episodes
3. ✅ Uses `technical` summary style (detailed explanations)
4. ✅ Prioritizes longer episodes with complex topics
5. ✅ Generates comprehensive summaries using GPT-4

---

## 🔬 How The Agentic Loop Works

```python
def run_with_visualization(self, user_goal: str, max_iterations: int = 10):
    """
    The core agentic loop.
    AI is in control, not hardcoded logic.
    """

    messages = [{
        "role": "user",
        "content": f"Your goal: {user_goal}\n\nThink strategically..."
    }]

    iteration = 0
    while iteration < max_iterations:
        # 1. AI PERCEIVES: Analyzes current state and goal
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=self.tools,        # Available tools
            tool_choice="auto"       # AI decides!
        )

        # 2. AI REASONS: Shows its thinking
        if response.message.content:
            print(f"💭 AI Reasoning: {response.message.content}")

        # 3. AI ACTS: Decides to use a tool
        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Execute REAL API calls based on AI's choice
                result = self.execute_tool(tool_name, tool_args)

                # 4. AI ADAPTS: Observes result and plans next action
                messages.append(tool_result)
                # Loop continues with new information...

        # AI decides goal is achieved
        elif response.finish_reason == "stop":
            return response.message.content
```

---

## 📊 Comparison to Original Project

### [Original Podcast Summarizer](https://github.com/jaskiran9941/llm-apps/tree/main/podcast-summarizer) (Non-Agentic)

**Architecture:**
```
You provide RSS URLs → Fetch all episodes → Get transcripts → Summarize all → Send email
```

**Characteristics:**
- ❌ **Control:** You write the script
- ❌ **Data:** You provide exact RSS feeds
- ❌ **Processing:** Processes everything equally
- ❌ **Adaptation:** Same behavior always
- ❌ **Intelligence:** No decision-making
- ✅ **Use case:** "Process these specific feeds on a schedule"

### This Agentic Version (Enhancement)

**Architecture:**
```
You give goal → AI searches iTunes → AI parses RSS → AI filters → AI adapts style → AI decides delivery
```

**Characteristics:**
- ✅ **Control:** AI decides autonomously
- ✅ **Data:** AI searches podcast databases (iTunes API)
- ✅ **Processing:** Intelligent filtering and prioritization
- ✅ **Adaptation:** Changes behavior based on context
- ✅ **Intelligence:** Reasons about what to do
- ✅ **Use case:** "Intelligently curate valuable insights for me"

**What Was Added:**
1. **AI Orchestrator** - GPT-4 makes decisions
2. **Tool Calling System** - AI selects appropriate actions
3. **Real Data Integration** - iTunes API, RSS parsing
4. **Context Awareness** - Adapts to user state and preferences
5. **Adaptive Behavior** - Changes strategy based on results

---

## 🎓 What You'll Learn

By studying this project, you'll understand:

### 1. What Makes Software "Agentic"
- **Autonomous decision-making** vs hardcoded control flow
- **Goal-oriented behavior** vs step execution
- **Dynamic adaptation** vs fixed behavior

### 2. How to Build AI Agents with OpenAI
- Tool calling / function calling API
- Agentic loop architecture (perceive → reason → act → adapt)
- Tool definition and execution patterns

### 3. Real-World Agent Applications
- When agents add value over automation
- How to integrate agents with real APIs
- Visualizing agent decision-making

### 4. Agent Design Patterns
- Goal-based prompting strategies
- Tool selection and prioritization
- Result observation and adaptation loops

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Brain** | GPT-4 Turbo (OpenAI) | Autonomous decision-making |
| **SDK** | OpenAI Python SDK | LLM API, tool calling |
| **Podcast Discovery** | iTunes Search API | Find podcasts (free, no key needed) |
| **Episode Fetching** | feedparser | Parse RSS feeds |
| **UI** | Streamlit | Visualize agent thinking |
| **Language** | Python 3.8+ | Implementation |

**No Heavy Frameworks:**
- ✅ Native OpenAI tool calling (no LangChain needed)
- ✅ Simple, readable code
- ✅ Real API integrations
- ✅ Educational focus

---

## 🎯 Why This Matters

### The Evolution of Automation

```
Level 1: Manual          Level 2: Automated       Level 3: Agentic (This!)
(You do everything)  →   (Script does steps)  →   (AI decides what to do)

You open podcast app     Script fetches all       AI searches for what
You search for shows     episodes from feeds      YOU care about
You read descriptions    Script summarizes all    AI filters by relevance
You decide what to read  Script sends email       AI adapts to your context
```

**This project demonstrates Level 3:** The AI agent makes intelligent decisions on your behalf.

---

## 📈 Real-World Applications

This agentic pattern can be applied to:

1. **Email Assistants**
   - AI decides which emails need responses
   - Chooses tone and detail level
   - Prioritizes by importance

2. **Research Assistants**
   - AI plans research strategy
   - Decides which sources to check
   - Adapts based on findings

3. **Content Curators**
   - AI filters by relevance
   - Chooses presentation style
   - Decides delivery timing

4. **Personal Assistants**
   - AI understands your context
   - Makes intelligent prioritization
   - Adapts to your current state

---

## 🔄 Evolution Path

This demonstrates a **simple agentic agent**. Future enhancements:

```
Current State          Next Level            Advanced
Simple Agent      →    Multi-Agent       →   MCP-Based
(This Project)         System                 Architecture

One AI decides         Specialized agents     Standardized
everything             work together          tool protocols

Complexity: ★★☆☆☆      Complexity: ★★★★☆     Complexity: ★★★☆☆
```

---

## 🚨 Known Limitations

1. **Time Window Issue**
   - Default 24-hour window often too short for podcast publishing
   - Most podcasts publish weekly or bi-weekly
   - Agent adapts by suggesting broader time ranges

2. **Subscriptions Hardcoded**
   - Currently 3 podcasts hardcoded in app_real.py:80-96
   - Should be moved to config file or database
   - Agent can discover new podcasts via iTunes search

3. **Summaries From Descriptions**
   - GPT-4 summarizes episode descriptions, not full transcripts
   - Original project has actual transcript fetching
   - Could be enhanced by integrating transcript tools

4. **No Persistence**
   - Saved episodes, preferences not stored
   - Each run starts fresh
   - Could add database layer

---

## 🤝 Contributing

This is a learning project! Feel free to:
- Add more sophisticated tools
- Implement memory/persistence
- Integrate actual transcript fetching
- Build multi-agent version
- Add more podcast APIs (Spotify, Listen Notes)

---

## 📚 Further Reading

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [iTunes Search API Documentation](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/)
- [Building AI Agents with OpenAI](https://platform.openai.com/docs/guides/agents)

---

## 📝 License

MIT License - Free to learn from and build upon!

---

## 🙏 Acknowledgments

**This project is an agentic enhancement of [podcast-summarizer](https://github.com/jaskiran9941/llm-apps/tree/main/podcast-summarizer).**

The original project demonstrated automated podcast processing. This enhancement demonstrates **what happens when you add autonomous AI decision-making** - transforming automation into true agentic behavior.

**Key Insight:** Making software "agentic" isn't about adding more features. It's about **transferring control from hardcoded logic to AI reasoning**. When the AI decides what to do based on goals and context, you have an agent. When you hardcode the decisions, you have automation.

---

**Happy Learning! 🤖**

*Watch an AI agent think, reason, and adapt in real-time.*
