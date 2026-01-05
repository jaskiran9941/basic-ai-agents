"""
Content Discovery Agent - Main orchestration file.

This is the core of our agent system. It uses Claude (Anthropic's LLM) with
tool calling to intelligently discover and curate content based on user topics.

Key Concepts Demonstrated:
1. ReAct Pattern: Reasoning (Claude thinks) + Acting (calls tools)
2. Tool Calling: LLM decides which tools to use
3. Multi-turn conversation: LLM can use multiple tools in sequence
4. Error handling: Graceful degradation when tools fail

Learning Objectives:
- Understand how agents differ from simple scripts
- See how LLMs make autonomous decisions
- Learn tool calling patterns
- Handle non-deterministic behavior
"""

import json
from typing import List, Dict, Any
import anthropic
from config import Config
from tools.web_search import web_search, WEB_SEARCH_TOOL
from tools.github_search import github_search, GITHUB_SEARCH_TOOL
from tools.books_search import books_search, BOOKS_SEARCH_TOOL
from tools.youtube_search import youtube_search, YOUTUBE_SEARCH_TOOL
from tools.reddit_search import reddit_search, REDDIT_SEARCH_TOOL
from tools.arxiv_search import arxiv_search, ARXIV_SEARCH_TOOL


class ContentDiscoveryAgent:
    """
    An AI agent that discovers and curates content based on user interests.

    This agent uses Claude with tool calling to:
    1. Understand the user's topic
    2. Decide which sources are relevant (web, GitHub, books, etc.)
    3. Search those sources
    4. Synthesize and rank results
    """

    def __init__(self):
        """Initialize the agent with Claude client and available tools."""
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.CLAUDE_MODEL

        # Available tools that Claude can use
        self.tools = [
            WEB_SEARCH_TOOL,
            GITHUB_SEARCH_TOOL,
            BOOKS_SEARCH_TOOL,
            YOUTUBE_SEARCH_TOOL,
            REDDIT_SEARCH_TOOL,
            ARXIV_SEARCH_TOOL
        ]

        # Tool execution mapping
        self.tool_functions = {
            "web_search": web_search,
            "github_search": github_search,
            "books_search": books_search,
            "youtube_search": youtube_search,
            "reddit_search": reddit_search,
            "arxiv_search": arxiv_search
        }

    def discover(self, topic: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Discover and curate content for a given topic.

        Args:
            topic: The topic to research (e.g., "AI Product Management")
            verbose: If True, print agent reasoning and tool calls

        Returns:
            Dict containing:
            - topic: Original topic
            - results: Curated content
            - tools_used: Which tools the agent decided to use
            - total_cost: Estimated cost in USD

        Example:
            >>> agent = ContentDiscoveryAgent()
            >>> result = agent.discover("AI Product Management")
            >>> print(result['results'])
        """
        if verbose:
            print(f"\n🤖 Agent analyzing topic: '{topic}'")
            print("=" * 60)

        # System prompt - tells Claude how to think like an agent
        system_prompt = """You are an expert content discovery agent. Your job is to help users find the best resources (blogs, articles, repositories, books, videos, etc.) on any topic they're interested in.

When given a topic:
1. First, reason about what types of content would be most valuable for this topic
2. Decide which tools to use based on the topic:
   - web_search: For current articles, blogs, general information
   - github_search: For technical topics where code/projects exist
   - books_search: For topics where deep reading or comprehensive guides help
   - youtube_search: For visual learning, tutorials, demonstrations
   - reddit_search: For community discussions, real user experiences
   - arxiv_search: For academic papers, research, cutting-edge developments
3. Call the appropriate tools to gather information
4. Synthesize the results into a curated, ranked list
5. Explain your reasoning

Important:
- Use multiple tools when appropriate (e.g., web + books + youtube for learning topics)
- Don't use GitHub or arXiv for non-technical topics (e.g., parenting, relationships)
- Don't use arXiv for beginner topics (it's for advanced research)
- Reddit is good for practical experiences and troubleshooting
- YouTube is great for visual/practical learning
- Be selective - quality over quantity (max 3-4 tools per query)

After gathering information, provide a structured summary with:
1. Overview of what you found
2. Top recommendations for each category
3. Why you chose these specific resources
4. Suggested order for consuming the content"""

        # Initial user message
        messages = [
            {
                "role": "user",
                "content": f"I want to learn about: {topic}\n\nPlease find me the best resources available."
            }
        ]

        # Track conversation and tool usage
        tools_used = []
        conversation_history = []

        try:
            # Agent loop - Claude can make multiple tool calls
            while True:
                # Call Claude with available tools
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=Config.MAX_TOKENS,
                    system=system_prompt,
                    messages=messages,
                    tools=self.tools,
                    temperature=Config.TEMPERATURE
                )

                # Track this interaction
                conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Check stop reason
                if response.stop_reason == "end_turn":
                    # Agent is done - extract final response
                    final_response = self._extract_text_response(response.content)
                    if verbose:
                        print(f"\n✅ Agent completed analysis\n")
                    break

                elif response.stop_reason == "tool_use":
                    # Agent wants to use tools
                    tool_results = []

                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_input = block.input
                            tool_id = block.id

                            if verbose:
                                print(f"\n🔧 Agent using tool: {tool_name}")
                                print(f"   Query: {tool_input.get('query', 'N/A')}")

                            # Execute the tool
                            result = self._execute_tool(tool_name, tool_input)
                            tools_used.append({
                                "tool": tool_name,
                                "query": tool_input.get('query', ''),
                                "success": result.get('success', False),
                                "raw_results": result.get('results', []),  # Store raw results
                                "total": result.get('total', 0)
                            })

                            if verbose:
                                if result.get('success'):
                                    print(f"   ✓ Found {result.get('total', 0)} results")
                                else:
                                    print(f"   ✗ Error: {result.get('error', 'Unknown')}")

                            # Format result for Claude
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": json.dumps(result)
                            })

                    # Add assistant's response and tool results to conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })

                    # Continue the loop - Claude will process results and decide next step

                else:
                    # Unexpected stop reason
                    if verbose:
                        print(f"\n⚠️  Unexpected stop reason: {response.stop_reason}")
                    break

            # Calculate estimated cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            estimated_cost = self._calculate_cost(input_tokens, output_tokens)

            if verbose:
                print(f"\n💰 Estimated cost: ${estimated_cost:.4f}")
                print(f"   Input tokens: {input_tokens:,}")
                print(f"   Output tokens: {output_tokens:,}")
                print("=" * 60)

            return {
                "topic": topic,
                "results": final_response,
                "tools_used": tools_used,
                "estimated_cost": estimated_cost,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens
                }
            }

        except Exception as e:
            if verbose:
                print(f"\n❌ Error: {str(e)}")

            return {
                "topic": topic,
                "results": f"Error occurred: {str(e)}",
                "tools_used": tools_used,
                "estimated_cost": 0,
                "error": str(e)
            }

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool function with given input."""
        if tool_name in self.tool_functions:
            return self.tool_functions[tool_name](**tool_input)
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "results": []
            }

    def _extract_text_response(self, content: List) -> str:
        """Extract text from Claude's response content blocks."""
        text_parts = []
        for block in content:
            if hasattr(block, 'type') and block.type == "text":
                text_parts.append(block.text)
        return "\n".join(text_parts)

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate estimated cost based on token usage.

        Claude 3.5 Sonnet pricing:
        - Input: $3 per million tokens
        - Output: $15 per million tokens
        """
        input_cost = (input_tokens / 1_000_000) * 3.0
        output_cost = (output_tokens / 1_000_000) * 15.0
        return input_cost + output_cost


def main():
    """Example usage of the Content Discovery Agent."""
    print("\n" + "=" * 60)
    print("Content Discovery Agent - Interactive Demo")
    print("=" * 60)

    agent = ContentDiscoveryAgent()

    # Example topics
    examples = [
        "AI Product Management",
        "making kids listen",
        "being a better partner after 9 years of marriage"
    ]

    print("\nExample topics:")
    for i, ex in enumerate(examples, 1):
        print(f"{i}. {ex}")

    print("\nOr enter your own topic.")

    topic = input("\nEnter a topic (or number): ").strip()

    # Handle number selection
    if topic.isdigit() and 1 <= int(topic) <= len(examples):
        topic = examples[int(topic) - 1]

    if not topic:
        print("No topic provided. Exiting.")
        return

    # Run the agent
    result = agent.discover(topic, verbose=True)

    # Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(result['results'])
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
