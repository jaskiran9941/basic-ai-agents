# Setup Guide - Content Discovery Agent

This guide will walk you through setting up the agent from scratch. Follow these steps carefully.

## Prerequisites

- Python 3.8 or higher
- Terminal/Command line access
- Internet connection
- Credit card for API signups (most have free tiers)

## Step 1: Install Python Dependencies

```bash
# Navigate to the project directory
cd /Users/jaskiran9941/Desktop/basic-ai-agents

# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Get API Keys

You need 4 API keys. I'll walk you through each one:

### 2.1 Anthropic API Key (Claude) - REQUIRED

**Why:** This is the brain of your agent. Claude decides which tools to use.

**Steps:**
1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Click "API Keys" in the left sidebar
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)

**Cost:**
- Input: $3 per million tokens
- Output: $15 per million tokens
- For testing this project: ~$0.50 - $2.00 total

**Free tier:** $5 credit for new users

---

### 2.2 Tavily Search API Key - REQUIRED

**Why:** Powers web search for finding blogs, articles, and current information.

**Steps:**
1. Go to: https://tavily.com/
2. Click "Get Started" or "Sign Up"
3. Verify your email
4. Go to your dashboard
5. Copy your API key

**Cost:**
- First 1000 searches: FREE
- After that: $1 per 1000 searches

**Free tier:** 1000 searches/month

---

### 2.3 GitHub Personal Access Token - REQUIRED

**Why:** Searches GitHub for code repositories and projects.

**Steps:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Content Discovery Agent"
4. Select scopes:
   - ✅ `public_repo` (for searching public repos)
   - That's all you need!
5. Click "Generate token" at the bottom
6. Copy the token (starts with `ghp_...`)

**Important:** Copy it now - you won't see it again!

**Cost:** FREE (unlimited for public repo searches)

---

### 2.4 Google Books API Key - REQUIRED

**Why:** Searches for relevant books and publications.

**Steps:**
1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Click "Enable APIs and Services"
4. Search for "Books API"
5. Click on "Books API" and click "Enable"
6. Go to "Credentials" in left sidebar
7. Click "Create Credentials" → "API Key"
8. Copy the API key

**Cost:** FREE (1000 requests per day)

---

## Step 3: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Open the .env file in a text editor
nano .env
# or
open .env
# or use VS Code, TextEdit, etc.
```

Paste your API keys into the `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
TAVILY_API_KEY=tvly-your-key-here
GITHUB_TOKEN=ghp_your-token-here
GOOGLE_BOOKS_API_KEY=your-google-key-here
```

**Save the file.**

## Step 4: Verify Setup

Test that everything is configured correctly:

```bash
python -c "from config import Config; Config.validate(); print('✅ All API keys configured correctly!')"
```

If you see errors, double-check:
1. Your API keys are correct
2. The `.env` file is in the right location
3. No extra spaces or quotes around the keys

## Step 5: Run Your First Test

```bash
# Run the interactive agent
python agent.py
```

Or run the test suite:

```bash
python examples/test_agent.py
```

## Troubleshooting

### "Module not found" errors
```bash
# Make sure you activated the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Missing required API keys"
- Check that your `.env` file exists
- Verify each API key is on its own line
- No quotes around the keys
- No spaces after the `=` sign

### "Authentication failed" for any API
- Verify the API key is correct
- Check if you need to activate the API (Google requires enabling)
- Ensure the key has proper permissions (GitHub token needs `public_repo`)

### Rate limit errors
- Tavily: You've exceeded 1000 searches in the free tier
- GitHub: You've exceeded 5000 requests/hour (very unlikely during testing)
- Google Books: You've exceeded 1000 requests/day

## Next Steps

Once setup is complete:

1. **Test with different topics** - See how the agent adapts
2. **Read the code** - Understand how tools and agents work
3. **Modify prompts** - Experiment with agent behavior
4. **Add new tools** - Try integrating another API
5. **Compare with Composio** - After mastering direct APIs

## Understanding Your First Run

When you run the agent, you'll see:

```
🤖 Agent analyzing topic: 'AI Product Management'
============================================================

🔧 Agent using tool: web_search
   Query: AI product management best practices blogs
   ✓ Found 5 results

🔧 Agent using tool: github_search
   Query: AI product management tools
   ✓ Found 5 results

🔧 Agent using tool: books_search
   Query: AI product management
   ✓ Found 5 results

✅ Agent completed analysis

💰 Estimated cost: $0.0234
   Input tokens: 2,456
   Output tokens: 891
============================================================
```

**Key observations:**
- The agent DECIDED to use all three tools (not hardcoded!)
- It crafted specific queries for each tool
- It cost only $0.02 to run
- Total time: ~5-10 seconds

## PM Learning Checkpoints

After setup, you should understand:

- ✅ **API Integration Basics** - How to get keys and authenticate
- ✅ **Environment Management** - Using .env for secrets
- ✅ **Dependency Management** - requirements.txt and virtual environments
- ✅ **Cost Awareness** - Tracking token usage and API costs

## Cost Summary for Testing

Expected costs for fully testing this project:

| API | Test Usage | Cost |
|-----|------------|------|
| Anthropic (Claude) | ~50 test runs | $1.00 - $2.00 |
| Tavily Search | ~30 searches | $0 (free tier) |
| GitHub API | ~30 searches | $0 (free) |
| Google Books API | ~30 searches | $0 (free) |
| **Total** | | **$1.00 - $2.00** |

**Bottom line:** You can fully build and test this project for about $2.

## Ready to Learn?

Proceed to:
1. `LEARNING_NOTES.md` - Understand agent concepts
2. `examples/test_agent.py` - See the agent in action
3. `agent.py` - Study the core architecture

Happy building!
