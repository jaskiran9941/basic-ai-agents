#!/usr/bin/env node

/**
 * Simple MCP Playwright Server
 * Provides browser automation tools via MCP
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { chromium } from 'playwright';

let browser = null;
let page = null;

// Create MCP server
const server = new Server(
  {
    name: 'playwright-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool: Navigate to URL
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'browser_navigate',
        description: 'Navigate to a URL in the browser',
        inputSchema: {
          type: 'object',
          properties: {
            url: {
              type: 'string',
              description: 'The URL to navigate to',
            },
          },
          required: ['url'],
        },
      },
      {
        name: 'browser_click',
        description: 'Click on an element matching the selector',
        inputSchema: {
          type: 'object',
          properties: {
            selector: {
              type: 'string',
              description: 'CSS selector for the element to click',
            },
          },
          required: ['selector'],
        },
      },
      {
        name: 'browser_screenshot',
        description: 'Take a screenshot of the current page',
        inputSchema: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'Path to save the screenshot',
            },
          },
        },
      },
      {
        name: 'browser_get_content',
        description: 'Get the text content of the current page',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'browser_fill',
        description: 'Fill a form field',
        inputSchema: {
          type: 'object',
          properties: {
            selector: {
              type: 'string',
              description: 'CSS selector for the input field',
            },
            value: {
              type: 'string',
              description: 'Value to fill in',
            },
          },
          required: ['selector', 'value'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  // Initialize browser if needed
  if (!browser) {
    browser = await chromium.launch({ headless: false });
    page = await browser.newPage();
  }

  try {
    switch (name) {
      case 'browser_navigate':
        await page.goto(args.url);
        return {
          content: [
            {
              type: 'text',
              text: `Navigated to ${args.url}`,
            },
          ],
        };

      case 'browser_click':
        await page.click(args.selector);
        return {
          content: [
            {
              type: 'text',
              text: `Clicked element: ${args.selector}`,
            },
          ],
        };

      case 'browser_screenshot':
        const path = args.path || 'screenshot.png';
        await page.screenshot({ path });
        return {
          content: [
            {
              type: 'text',
              text: `Screenshot saved to ${path}`,
            },
          ],
        };

      case 'browser_get_content':
        const content = await page.textContent('body');
        return {
          content: [
            {
              type: 'text',
              text: content,
            },
          ],
        };

      case 'browser_fill':
        await page.fill(args.selector, args.value);
        return {
          content: [
            {
              type: 'text',
              text: `Filled ${args.selector} with value`,
            },
          ],
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Cleanup on exit
  process.on('SIGINT', async () => {
    if (browser) {
      await browser.close();
    }
    process.exit(0);
  });
}

main().catch(console.error);
