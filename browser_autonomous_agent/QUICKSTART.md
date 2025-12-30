# 🚀 Quick Start Guide

## Get Up and Running in 3 Steps

### Step 1: Set Your API Key

Edit the `.env` file and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

Or export it in your terminal:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

### Step 2: Launch the Streamlit UI

```bash
./run_streamlit.sh
```

Or manually:

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

### Step 3: Start Controlling the Browser

1. Open http://localhost:8501 in your browser
2. Enter your API key in the sidebar (if not already set)
3. Type a command like:
   - `"Go to https://github.com"`
   - `"Click the search button"`
   - `"Take a screenshot"`

## What to Expect

### The Streamlit Interface

```
┌─────────────────────────────────────────────────────────┐
│  🌐 Browser MCP Agent                                   │
├───────────────────────────────┬─────────────────────────┤
│  💬 Command Interface         │  📸 Browser Preview     │
│                               │                         │
│  You: Go to GitHub            │  [Screenshot appears]   │
│  🤖: Navigating to            │                         │
│      https://github.com       │  ⬇️ Download            │
│                               │                         │
│  [Type command here...]       │                         │
└───────────────────────────────┴─────────────────────────┘
```

### The Browser Window

- A **separate Chrome window will open** (non-headless mode)
- You'll see it navigate, click, and interact in real-time
- Watch as the agent executes your commands
- Screenshots are automatically saved and displayed in the UI

## Example Session

```
You: "Go to https://github.com"
🤖: Navigating to GitHub...
[Browser opens and loads GitHub]

You: "Click the search bar and search for 'claude-agent-sdk'"
🤖: Clicking search bar and typing...
[Browser clicks search, types the query]

You: "Take a screenshot"
🤖: Taking screenshot...
[Screenshot appears in the right panel]
```

## Troubleshooting

### "Browser not connecting"
- Make sure the MCP Playwright server is running
- Check that Node.js dependencies are installed (`npm install`)
- Verify Playwright is installed (`npx playwright install chromium`)

### "API key error"
- Ensure your API key is set in `.env` or the sidebar
- Check that it starts with `sk-ant-`

### "Command not executing"
- The Streamlit version uses a simplified implementation
- For full MCP integration, see the note below

## Note: Current Implementation

The Streamlit UI currently uses the **Anthropic API directly** to interpret commands and explain what actions would be taken.

To enable **actual browser control** via MCP, you would need to:
1. Use the Python Claude Agent SDK (requires Python 3.10+)
2. Or call the TypeScript agent via subprocess (requires additional setup)

For now, the app demonstrates the UI and command interface. The CLI mode (`npm start`) has full MCP browser control capabilities.

## Next Steps

- Try the CLI mode for full browser automation: `npm start`
- Extend the Streamlit UI to call the TypeScript agent
- Add more browser tools (scroll, wait for elements, etc.)
- Integrate with other MCP servers (filesystem, GitHub, etc.)

Enjoy controlling your browser with natural language! 🎉
