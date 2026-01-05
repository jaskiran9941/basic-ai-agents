# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├──────────────────────────────┬──────────────────────────────────┤
│   🖥️  CLI Mode               │   🌐 Streamlit Web UI            │
│   (src/agent.ts)             │   (streamlit_app.py)             │
│                              │                                  │
│   Terminal Input/Output      │   Web Browser Interface          │
│   - Type commands            │   - Chat interface               │
│   - See real-time logs       │   - Screenshot preview           │
│   - Watch browser            │   - Command history              │
└──────────────┬───────────────┴──────────────┬───────────────────┘
               │                              │
               │                              │
               ▼                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CLAUDE AGENT SDK                              │
│                  (@anthropic-ai/claude-agent-sdk)                │
│                                                                  │
│  • Orchestrates agent behavior                                  │
│  • Manages conversation context                                 │
│  • Handles tool selection & execution                           │
│  • Streams responses back to user                               │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               │ query({ prompt, options })
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                   MODEL CONTEXT PROTOCOL (MCP)                   │
│                                                                  │
│  Configuration (.mcp.json):                                     │
│  {                                                              │
│    "mcpServers": {                                              │
│      "playwright": {                                            │
│        "command": "node",                                       │
│        "args": ["mcp-playwright-server.js"]                     │
│      }                                                          │
│    }                                                            │
│  }                                                              │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               │ stdio communication
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│              MCP PLAYWRIGHT SERVER                               │
│              (mcp-playwright-server.js)                          │
│                                                                  │
│  Exposed Tools:                                                 │
│  ┌────────────────────────────────────────────────┐            │
│  │ mcp__playwright__browser_navigate              │            │
│  │ mcp__playwright__browser_click                 │            │
│  │ mcp__playwright__browser_fill                  │            │
│  │ mcp__playwright__browser_screenshot            │            │
│  │ mcp__playwright__browser_get_content           │            │
│  └────────────────────────────────────────────────┘            │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               │ Playwright API
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      PLAYWRIGHT                                  │
│                                                                  │
│  • Launches Chromium browser                                    │
│  • Controls browser actions                                     │
│  • Captures screenshots                                         │
│  • Extracts page content                                        │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                   CHROMIUM BROWSER                               │
│                                                                  │
│  • Visible window (non-headless)                                │
│  • Executes actions in real-time                                │
│  • Renders web pages                                            │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Command Flow

```
User Types: "Go to GitHub and take a screenshot"
     ↓
Agent SDK receives prompt
     ↓
Claude analyzes command and determines needed tools
     ↓
MCP Protocol sends tool requests:
  1. mcp__playwright__browser_navigate(url: "https://github.com")
  2. mcp__playwright__browser_screenshot()
     ↓
Playwright Server executes:
  1. page.goto("https://github.com")
  2. page.screenshot({path: "screenshot.png"})
     ↓
Browser performs actions
     ↓
Results flow back through MCP
     ↓
Agent SDK streams responses to user
     ↓
User sees: "✓ Navigated to GitHub" and "✓ Screenshot saved"
```

## Component Details

### CLI Agent (src/agent.ts)

```typescript
┌─────────────────────────────────────┐
│  Interactive Command Loop           │
│                                     │
│  1. Read user input                 │
│  2. Call query() with prompt        │
│  3. Stream responses                │
│  4. Display tool executions         │
│  5. Show results                    │
│  6. Repeat                          │
└─────────────────────────────────────┘
```

**Key Features:**
- Readline interface for input
- Real-time streaming output
- Tool execution visibility
- Error handling

### MCP Server (mcp-playwright-server.js)

```javascript
┌─────────────────────────────────────┐
│  MCP Server Implementation          │
│                                     │
│  Handlers:                          │
│  • tools/list → Returns tool defs   │
│  • tools/call → Executes tool       │
│                                     │
│  State:                             │
│  • browser (Playwright instance)    │
│  • page (Current page)              │
└─────────────────────────────────────┘
```

**Tool Definition Example:**
```javascript
{
  name: 'browser_navigate',
  description: 'Navigate to a URL',
  inputSchema: {
    type: 'object',
    properties: {
      url: { type: 'string', description: 'URL to visit' }
    },
    required: ['url']
  }
}
```

### Streamlit UI (streamlit_app.py)

```
┌─────────────────────────────────────┐
│  Streamlit Web Application          │
│                                     │
│  Layout:                            │
│  ┌─────────┬──────────────────┐    │
│  │ Sidebar │  Main Content    │    │
│  │         │                  │    │
│  │ • API   │ • Chat interface │    │
│  │   Key   │ • Message history│    │
│  │ • Status│ • Input box      │    │
│  │ • Help  │ • Screenshots    │    │
│  └─────────┴──────────────────┘    │
│                                     │
│  Session State:                     │
│  • messages[]                       │
│  • browser_status                   │
└─────────────────────────────────────┘
```

## MCP Communication Protocol

```
Agent SDK                    MCP Server
    │                            │
    │──── tools/list ──────────→ │
    │                            │
    │ ←──── tool definitions ──── │
    │                            │
    │──── tools/call ──────────→ │
    │  {name, arguments}         │
    │                            │
    │     [tool executes]        │
    │                            │
    │ ←──── result ──────────────│
    │  {content, isError}        │
```

## File Organization

```
browser_mcp_agent/
│
├── 🎯 Core Agent
│   ├── src/agent.ts              # TypeScript CLI agent
│   └── streamlit_app.py          # Python web UI
│
├── 🔧 MCP Integration
│   ├── mcp-playwright-server.js  # Custom MCP server
│   ├── .mcp.json                 # Server configuration
│   └── agent_executor.py         # Python-TS bridge
│
├── ⚙️ Configuration
│   ├── package.json              # Node dependencies
│   ├── requirements.txt          # Python dependencies
│   ├── tsconfig.json             # TypeScript config
│   ├── .env                      # API keys (gitignored)
│   └── .env.example              # Template
│
├── 📚 Documentation
│   ├── README.md                 # Main documentation
│   ├── QUICKSTART.md             # Quick start guide
│   ├── PROJECT_SUMMARY.md        # What you learned
│   └── ARCHITECTURE.md           # This file
│
└── 🚀 Launchers
    └── run_streamlit.sh          # Streamlit launcher
```

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  CLI (TypeScript) + Web UI (Python)     │
├─────────────────────────────────────────┤
│         Orchestration Layer             │
│      Claude Agent SDK (TypeScript)      │
├─────────────────────────────────────────┤
│         Protocol Layer                  │
│    Model Context Protocol (MCP)         │
├─────────────────────────────────────────┤
│         Tool Layer                      │
│    Custom MCP Playwright Server         │
├─────────────────────────────────────────┤
│         Automation Layer                │
│          Playwright Library             │
├─────────────────────────────────────────┤
│         Browser Layer                   │
│        Chromium Browser                 │
└─────────────────────────────────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────┐
│  Security Layers                    │
│                                     │
│  1. API Key Management              │
│     • .env file (gitignored)        │
│     • Environment variables         │
│     • Never committed to git        │
│                                     │
│  2. Tool Permissions                │
│     • allowedTools whitelist        │
│     • permissionMode config         │
│                                     │
│  3. Browser Isolation               │
│     • Separate browser instance     │
│     • Clean slate each run          │
│                                     │
│  4. Input Validation                │
│     • MCP schema validation         │
│     • Type checking (TypeScript)    │
└─────────────────────────────────────┘
```

## Extensibility Points

### 1. Add New Browser Tools
Edit `mcp-playwright-server.js`:
```javascript
{
  name: 'browser_scroll',
  description: 'Scroll the page',
  inputSchema: { ... }
}
```

### 2. Add New MCP Servers
Edit `.mcp.json`:
```json
{
  "mcpServers": {
    "playwright": { ... },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem"]
    }
  }
}
```

### 3. Customize Agent Behavior
Edit `src/agent.ts`:
```typescript
options: {
  mcpServers,
  allowedTools: [...],
  permissionMode: 'acceptEdits',
  model: 'claude-sonnet-4',  // Change model
  maxTokens: 2000             // Adjust limits
}
```

## Performance Characteristics

| Component | Latency | Resource Usage |
|-----------|---------|---------------|
| MCP Server Startup | ~100ms | Low (1 process) |
| Browser Launch | ~2-3s | Medium (Chromium) |
| Tool Call | ~500ms-2s | Depends on action |
| Agent Response | ~1-3s | Low (API call) |
| Screenshot Capture | ~200-500ms | Low (single image) |

## Error Handling Flow

```
User Command
    ↓
    ├─→ API Key Missing → Error in UI
    │
    ├─→ Invalid Command → Agent explains issue
    │
    ├─→ Tool Execution Fails
    │   └─→ MCP Server returns {isError: true}
    │       └─→ Agent SDK receives error
    │           └─→ User sees error message
    │
    └─→ Browser Timeout → Caught by Playwright
        └─→ Returned as MCP error
```

This architecture provides a solid foundation for building browser automation agents with MCP!
