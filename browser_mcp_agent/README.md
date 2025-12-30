# Browser Autonomous Agent

A true autonomous browser agent that can achieve complex goals without human intervention, powered by GPT-4 and Playwright.

## What Makes This a Real Agent?

Unlike simple command executors, this is a **true autonomous agent** that:

### ✅ Autonomous Agent (What This Is)
```
You: "Go to GitHub and find the top 3 trending Python repos"

Agent: [Thinks] I need to:
       1. Navigate to github.com
       2. Find the trending section
       3. Filter by Python
       4. Extract top 3 repos

Agent: [Autonomously executes 8 actions]
       ✓ Navigated to GitHub
       ✓ Clicked "Explore"
       ✓ Clicked "Trending"
       ✓ Selected Python filter
       ✓ Scrolled to load results
       ✓ Extracted repo names

Agent: "Complete! Found: django, flask, fastapi"
```

### ❌ NOT a Command Executor
This is NOT a tool where you manually tell it each step.

## Key Capabilities

**Autonomous Operation:**
- 🎯 **Goal-Oriented** - Give it a goal, not step-by-step instructions
- 🧠 **Self-Planning** - Agent decides what actions to take
- 🔄 **Adaptive** - Responds to page content and adjusts strategy
- 📊 **Multi-Step Execution** - Completes complex workflows autonomously
- ✅ **Auto-Completion** - Knows when the goal is achieved

**Also Supports Simple Commands:**
- 💬 **Command Mode** - For simple single actions
- 🔮 **Auto Detection** - Automatically knows if you want command or goal
- 📝 **Flexible Input** - Works with both modes seamlessly

## Tech Stack

- **OpenAI GPT-4** - Natural language command interpretation
- **Playwright (Async)** - Browser automation with thread-safe event loops
- **Streamlit** - Interactive web UI
- **Python 3.9+** - Modern async/await patterns

## Setup

### Prerequisites
- Python 3.9 or higher
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jaskiran9941/browser_mcp_agent.git
   cd browser_mcp_agent
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

5. **Set up your OpenAI API key:**

   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your-api-key-here
   ```

   Or export it:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

### Running the Streamlit Web UI

1. **Start the application:**
   ```bash
   ./run_streamlit.sh
   ```

   Or manually:
   ```bash
   source venv/bin/activate
   streamlit run streamlit_app.py
   ```

2. **Open in your browser:**
   - Navigate to http://localhost:8501

3. **Using the interface:**
   - Your OpenAI API key will be auto-loaded from `.env`
   - Enter a starting URL (e.g., https://github.com)
   - Click "Open Browser" - a Chrome window will appear
   - Type commands in the chat input
   - Watch commands execute live in the browser window

## Example Goals vs Commands

### 🎯 Autonomous Goals (Agent Mode)

Give high-level objectives - the agent figures out how:

```
"Find the 3 most popular Python web frameworks on GitHub"
→ Agent navigates, searches, filters, scrolls, extracts

"Go to Hacker News and get the top 5 story titles"
→ Agent navigates, finds stories, extracts titles, reports back

"Search Reddit for 'AI agents' and click the first post"
→ Agent navigates, uses search, identifies first result, clicks

"Compare the star counts of django vs flask on GitHub"
→ Agent searches both, extracts stars, compares, reports
```

### 💬 Simple Commands (Command Mode)

For single actions:

```
"scroll down"
"go to reddit.com"
"click the search button"
"fill the search box with 'hello'"
```

## Who Should Use This?

### Perfect For:

**1. Developers**
- Automate repetitive testing workflows
- Web scraping with natural language
- Automated data collection from multiple sites
- Testing web applications without writing Selenium code

**2. Researchers**
- Collect data from websites autonomously
- Monitor websites for changes
- Extract information across multiple pages

**3. Product Managers / QA**
- Test user flows without coding
- Verify features across different scenarios
- Automated regression testing with plain English

**4. Anyone Who Needs Browser Automation**
- No programming required for basic automation
- Natural language instead of CSS selectors
- Quick prototyping of automation workflows

## How The Agent Works

### Goal Mode (Autonomous)
1. **You give a goal** - "Find the top 3 Python repos on GitHub"
2. **Agent analyzes** - Understands what needs to be done
3. **Agent plans** - Breaks goal into steps
4. **Agent loops:**
   - Reads current page content
   - Decides next action
   - Executes action
   - Evaluates if goal is complete
   - Repeats until done
5. **Agent reports** - "Complete! Found: django, flask, fastapi"

### Command Mode (Manual)
1. **You type a command** - "scroll down"
2. **GPT-4 interprets** - Converts to action
3. **Playwright executes** - Performs action
4. **You see result** - Action feedback

## UI Features

- 🤖 **Three Modes**: Command (manual), Goal (autonomous), Auto (smart detection)
- 📊 **Progress Tracking** - See each step the agent takes
- 💬 **Chat Interface** - Conversational interaction
- 🟢 **Browser Status** - Live connection indicator
- 📝 **Action History** - Full log of what agent did
- 💡 **Built-in Examples** - Learn by example

## Project Structure

```
browser_mcp_agent/
├── streamlit_app.py            # Main Streamlit web UI with async Playwright
├── run_streamlit.sh            # Streamlit launcher script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── .env.example                # Example environment file
└── venv/                       # Python virtual environment
```

## Technical Implementation

### Autonomous Agent Architecture

**Agent Loop (Goal Mode):**
```python
while not goal_complete and steps < max_steps:
    1. Read page state (URL, title, content)
    2. Send to GPT-4: "Given goal X and current state Y, what's next?"
    3. GPT-4 responds with:
       - {"action": "click", "selector": "...", "reasoning": "..."}
       - OR {"status": "complete", "summary": "..."}
    4. Execute action
    5. Update page state
    6. Repeat
```

**Key Features:**
- **Page-Aware** - Agent sees current page content before deciding
- **Self-Correcting** - Can adapt if actions don't work as expected
- **Goal-Tracking** - Knows when objective is achieved
- **Conversation Memory** - Remembers previous actions to avoid loops

### Thread-Safe Async Architecture

Solves Streamlit + Playwright threading issues:

- **Dedicated Event Loop Thread** - Persistent asyncio loop in background
- **Async Playwright API** - All browser ops use `async_playwright()`
- **Thread-Safe Execution** - `asyncio.run_coroutine_threadsafe()`
- **Persistent Objects** - Browser stays in same event loop

### Mode Detection

Auto mode intelligently detects intent:
- Keywords: "find", "search for", "get the", "compare" → Goal mode
- Length: > 10 words → Likely a goal
- Otherwise → Command mode

## Troubleshooting

**Browser won't start:**
- Make sure Chromium is installed: `playwright install chromium`
- Check that your OpenAI API key is set

**Thread/loop errors:**
- Click "Close Browser" in sidebar
- Click "Open Browser" to restart with fresh connection

**Commands not working:**
- Try being more specific with selectors
- Check the browser window for actual page state
- Use simpler commands first (scroll, navigate) before complex clicks

## Requirements

The `requirements.txt` includes:
- `streamlit` - Web UI framework
- `playwright` - Browser automation
- `openai` - GPT-4 API client
- `anthropic` - (Optional) For future Claude integration
- `requests` - HTTP library

## Future Enhancements

- Add screenshot capture and display
- Support for multiple browser tabs
- Command history persistence
- Visual element selection
- Macro recording and playback
- Integration with Claude API for improved command understanding

## License

MIT
