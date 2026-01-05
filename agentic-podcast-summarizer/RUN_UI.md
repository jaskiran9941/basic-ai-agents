# 🎨 How to Run the Streamlit UI

## Quick Start

```bash
# 1. Navigate to the project
cd basic-ai-agents/agentic-podcast-summarizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export ANTHROPIC_API_KEY='your-key'  # For Claude
# OR
export OPENAI_API_KEY='your-key'     # For GPT-4

# 4. Run the UI
streamlit run streamlit_app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 🎯 What You'll See

### Main Interface

The UI has 3 tabs:

#### 1. **🤖 Run Agent** (Main tab)
- Enter your goal
- Watch the AI make decisions in real-time
- See reasoning, tool choices, and results

#### 2. **📊 Comparison**
- Side-by-side comparison of agentic vs non-agentic
- Decision-making differences
- Interactive tables

#### 3. **❓ What Makes It Agentic?**
- The 5 core characteristics
- Expandable sections with examples
- Educational content

---

## 🔍 What Happens When You Run It

### Example Output:

```
🔄 Iteration 1
├── 💭 AI Reasoning:
│   "I should start by checking the user's preferences
│    to understand what topics they value..."
│
├── 🔧 Tool Selection:
│   Agent chose: check_user_preferences
│   Input: {}
│
└── ✅ Result:
    {
      "preferences": {
        "recent_topics": ["AI", "productivity"],
        "preferred_length": "brief"
      }
    }

🔄 Iteration 2
├── 💭 AI Reasoning:
│   "User likes AI and wants brief summaries.
│    Let me fetch episodes and filter for AI content..."
│
├── 🔧 Tool Selection:
│   Agent chose: fetch_new_episodes
│   Input: {"hours_back": 24}
│
└── ✅ Result:
    {"episodes": [...], "count": 3}

🔄 Iteration 3
├── 💭 AI Reasoning:
│   "Episode 1 is about AI (relevant), Episode 2 is cooking (skip).
│    I'll analyze relevance scores..."
│
└── ... continues until goal achieved
```

---

## 🎛️ UI Features

### Sidebar Configuration
- ✅ API key input (secure, password field)
- ✅ Quick goal presets:
  - 📌 Busy User
  - 🔍 Discovery Mode
  - 🎓 Deep Dive
- ✅ About section explaining agentic behavior

### Main Controls
- **Goal input**: Natural language description of what you want
- **Max iterations slider**: Control how long agent runs (5-20)
- **Run button**: Starts the agentic workflow

### Real-Time Visualization
- **Progress bar**: Shows iteration progress
- **Expandable sections**: Each iteration in collapsible panel
- **Color-coded boxes**:
  - 🟢 Green = AI Reasoning
  - 🔵 Blue = Tool Selection
  - 🟠 Orange = Results

---

## 🎮 Try These Scenarios

### Scenario 1: Busy User
**Goal:** "I'm extremely busy this week. Only send me insights if there's something genuinely important about AI. Keep it brief."

**Watch for:**
- AI checks preferences first ✓
- AI filters aggressively (skips cooking episode) ✓
- AI chooses "brief" summary style ✓
- AI decides whether to send or save for later ✓

### Scenario 2: Discovery Mode
**Goal:** "I want to learn about AI safety. Find relevant content or suggest new podcasts."

**Watch for:**
- AI searches current subscriptions ✓
- AI proactively searches web for new podcasts ✓
- AI prioritizes safety-specific content ✓
- AI provides recommendations ✓

### Scenario 3: Deep Dive
**Goal:** "I have time this weekend for technical content about AI. Give me detailed summaries."

**Watch for:**
- AI identifies "has time" context ✓
- AI chooses "detailed" or "technical" styles ✓
- AI includes more comprehensive content ✓

---

## 🔄 Multi-Provider Version

Want to use OpenAI instead of Anthropic?

```bash
# Run the multi-provider version
streamlit run streamlit_app_multi.py
```

This version lets you choose:
- **Anthropic Claude** (recommended - better tool calling)
- **OpenAI GPT-4** (also supports tool calling)

Switch providers in the sidebar!

---

## 🎨 Visual Elements

### What You'll See:

**Before running:**
- Clean interface with goal input
- Preset buttons for common scenarios
- Configuration in sidebar

**While running:**
- Progress bar showing iteration count
- Expanding sections for each decision cycle
- Color-coded boxes for different elements
- JSON viewers for tool inputs/outputs

**After completion:**
- Success message with final result
- Balloons animation 🎈
- Full execution history preserved
- Ability to run again with different goal

---

## 💡 Educational Value

The UI is designed to teach you about agentic AI:

1. **Transparent Reasoning**: See HOW the AI thinks
2. **Decision Visibility**: Understand WHY it chose each tool
3. **Comparison Mode**: Learn the difference vs non-agentic
4. **Interactive Learning**: Try different scenarios

---

## 🐛 Troubleshooting

### "API Key not found"
```bash
# Set environment variable
export ANTHROPIC_API_KEY='your-key'

# Or create .env file
echo "ANTHROPIC_API_KEY=your-key" > .env
```

### "Module not found: streamlit"
```bash
pip install streamlit
```

### "Port already in use"
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Want to see backend logs?
```bash
# Run with verbose logging
streamlit run streamlit_app.py --logger.level=debug
```

---

## 🎓 Next Steps

After exploring the UI:

1. **Read the code**: `streamlit_app.py` to understand implementation
2. **Modify scenarios**: Change the presets to test edge cases
3. **Add tools**: Extend with your own tool definitions
4. **Connect real data**: Replace mock data with actual podcast feeds

---

## 🎬 Demo Video

**Expected flow:**

1. Open UI → see clean interface
2. Keep default goal or choose preset
3. Click "Run Agent"
4. Watch iterations expand one by one
5. See AI reasoning → tool choice → result
6. Final completion with balloons!

**Total time:** ~30-60 seconds depending on iterations

---

## ⚡ Performance Tips

- **Fewer iterations** = faster results (try 5-8 for demos)
- **Claude** tends to be slightly faster than GPT-4
- **Mock data** means no API calls for tools (only LLM calls)

---

## 📱 Mobile Friendly?

Yes! Streamlit is responsive:
- Works on tablets
- Simplified layout on phones
- All features accessible

---

**Ready to see the agent think? Run `streamlit run streamlit_app.py` now!** 🚀
