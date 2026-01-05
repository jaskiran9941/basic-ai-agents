/**
 * Browser MCP Agent
 * Controls a web browser using natural language commands via MCP and Claude
 */

import { query } from '@anthropic-ai/claude-agent-sdk';
import * as readline from 'readline/promises';

// MCP server configuration for Playwright
const mcpServers = {
  playwright: {
    command: 'node',
    args: ['mcp-playwright-server.js'],
  },
};

// Available browser tools
const allowedTools = [
  'mcp__playwright__browser_navigate',
  'mcp__playwright__browser_click',
  'mcp__playwright__browser_screenshot',
  'mcp__playwright__browser_get_content',
  'mcp__playwright__browser_fill',
];

/**
 * Execute a browser command using the agent
 */
async function executeBrowserCommand(command: string) {
  console.log(`\n🤖 Processing: "${command}"\n`);

  try {
    // Stream responses from the agent
    for await (const message of query({
      prompt: command,
      options: {
        mcpServers,
        allowedTools,
        permissionMode: 'acceptEdits',
      },
    })) {
      if (message.type === 'assistant' && message.message?.content) {
        for (const block of message.message.content) {
          if ('text' in block) {
            console.log('✓', block.text);
          }
        }
      }

      if (message.type === 'tool_use' && message.message?.content) {
        for (const block of message.message.content) {
          if ('name' in block && block.type === 'tool_use') {
            console.log(`🔧 Using tool: ${block.name}`);
          }
        }
      }
    }
  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : error);
  }
}

/**
 * Interactive CLI for the browser agent
 */
async function main() {
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║         Browser MCP Agent - Powered by Claude            ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  console.log('\nControl your browser with natural language commands!\n');
  console.log('Examples:');
  console.log('  - "Go to https://github.com"');
  console.log('  - "Click on the search button"');
  console.log('  - "Get the page content"');
  console.log('  - "Take a screenshot and save it as test.png"');
  console.log('\nType "exit" to quit.\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  while (true) {
    const command = await rl.question('🌐 Enter command: ');

    if (command.trim().toLowerCase() === 'exit') {
      console.log('\n👋 Goodbye!');
      rl.close();
      break;
    }

    if (!command.trim()) {
      continue;
    }

    await executeBrowserCommand(command);
  }
}

// Run the agent
main().catch(console.error);
