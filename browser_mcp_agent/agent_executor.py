"""
Agent Executor - Runs the TypeScript browser agent from Python
"""

import subprocess
import json
import os
from typing import Optional

def execute_browser_command_via_agent(command: str, api_key: Optional[str] = None) -> str:
    """
    Execute a browser command by calling the TypeScript agent
    """
    try:
        # Set environment variable for API key
        env = os.environ.copy()
        if api_key:
            env["ANTHROPIC_API_KEY"] = api_key

        # Create a temporary script to run single command
        script_content = f"""
import {{ query }} from '@anthropic-ai/claude-agent-sdk';

const mcpServers = {{
  playwright: {{
    command: 'node',
    args: ['mcp-playwright-server.js'],
  }},
}};

const allowedTools = [
  'mcp__playwright__browser_navigate',
  'mcp__playwright__browser_click',
  'mcp__playwright__browser_screenshot',
  'mcp__playwright__browser_get_content',
  'mcp__playwright__browser_fill',
];

async function run() {{
  let output = '';

  for await (const message of query({{
    prompt: {json.dumps(command)},
    options: {{
      mcpServers,
      allowedTools,
      permissionMode: 'acceptEdits',
    }},
  }})) {{
    if (message.type === 'assistant' && message.message?.content) {{
      for (const block of message.message.content) {{
        if ('text' in block) {{
          output += block.text + '\\n';
        }}
      }}
    }}
  }}

  console.log(output);
}}

run().catch(console.error);
"""

        # Write temporary script
        with open('/tmp/browser_command.mjs', 'w') as f:
            f.write(script_content)

        # Execute the script
        result = subprocess.run(
            ['node', '/tmp/browser_command.mjs'],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )

        if result.returncode == 0:
            return result.stdout.strip() or "Command executed successfully"
        else:
            return f"Error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "Command timed out after 60 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"
