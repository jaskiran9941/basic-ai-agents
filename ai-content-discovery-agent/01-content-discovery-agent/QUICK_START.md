# Quick Start - Get Running in 10 Minutes

Already know what you're doing? Here's the express setup.

## 1. Install Dependencies (2 min)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Get API Keys (5 min)

| Service | Link | Cost |
|---------|------|------|
| Anthropic | https://console.anthropic.com/ | $5 free credit |
| Tavily | https://tavily.com/ | 1000 free searches |
| GitHub | https://github.com/settings/tokens | Free |
| Google Books | https://console.cloud.google.com/ | Free |

## 3. Configure (1 min)

```bash
cp .env.example .env
# Edit .env with your keys
```

## 4. Run (30 sec)

```bash
python agent.py
```

## Common Commands

```bash
# Run interactive agent
python agent.py

# Run test suite
python examples/test_agent.py

# Verify setup
python -c "from config import Config; Config.validate(); print('✅ Setup OK')"

# Check project structure
tree -L 2
```

## Test Your First Query

```python
from agent import ContentDiscoveryAgent

agent = ContentDiscoveryAgent()
result = agent.discover("AI Product Management")
print(result['results'])
```

## What You Should See

```
🤖 Agent analyzing topic: 'AI Product Management'
============================================================

🔧 Agent using tool: web_search
   Query: AI product management best practices
   ✓ Found 5 results

🔧 Agent using tool: github_search
   Query: AI product management
   ✓ Found 5 results

🔧 Agent using tool: books_search
   Query: AI product management
   ✓ Found 5 results

✅ Agent completed analysis

💰 Estimated cost: $0.0234
============================================================
```

## Troubleshooting

**"Module not found"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Missing API keys"**
- Check `.env` file exists
- Verify keys are correct
- No quotes or extra spaces

**"Authentication failed"**
- Double-check the specific API key
- GitHub: Need `public_repo` scope
- Google: Enable Books API first

## Next Steps

1. Read `LEARNING_NOTES.md` - Understand what you're building
2. Read `agent.py` - See the agent architecture
3. Test different topics - Watch the agent adapt
4. Modify and experiment - Best way to learn

## Files to Read (In Order)

1. `LEARNING_NOTES.md` - Conceptual understanding
2. `agent.py` - Core agent logic
3. `tools/web_search.py` - Example tool implementation
4. `SETUP_GUIDE.md` - Detailed setup if you get stuck

## Key Files

```
agent.py              # Main agent orchestration
config.py             # Configuration
tools/                # Tool implementations
examples/test_agent.py # Test suite
```

Ready to learn? Start with `LEARNING_NOTES.md`!
