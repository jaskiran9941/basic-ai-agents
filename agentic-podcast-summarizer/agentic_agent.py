#!/usr/bin/env python3
"""
Agentic Podcast Summarizer - Option 1: Simple Agentic Upgrade

This is an AGENTIC extension of the basic podcast-summarizer.
Instead of following a fixed script, the AI DECIDES what to do based on context.

WHY THIS IS AN AGENT:
====================
1. Autonomous Decision-Making: The AI chooses which tools to use and when
2. Goal-Oriented Behavior: Works toward user's goal, not just executing steps
3. Dynamic Tool Selection: Selects appropriate tools based on context
4. Adaptive Behavior: Changes strategy based on results
5. Reasoning & Planning: Thinks about the best approach before acting

KEY DIFFERENCES FROM NON-AGENTIC VERSION:
==========================================
Non-Agentic (podcast-summarizer):
  - YOU write: fetch() -> summarize() -> email()
  - Fixed pipeline, always same steps
  - No decision-making

Agentic (this version):
  - AI writes: "Should I check preferences first? Which episodes matter? What style?"
  - Dynamic workflow based on context
  - AI makes decisions at each step
"""

from anthropic import Anthropic
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class AgenticPodcastSummarizer:
    """
    AI Agent that intelligently manages podcast research and summarization.

    This is an AGENT because it:
    - Decides autonomously what to do next (not scripted)
    - Uses tools dynamically based on context
    - Adapts to user preferences and goals
    - Reasons about the best approach
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agentic system."""
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

        # Mock implementations of podcast tools
        # In production, these would import from your actual podcast-summarizer modules
        self.user_preferences = {
            "recent_topics": ["AI", "productivity", "technology"],
            "preferred_length": "detailed",
            "active_time": "morning",
            "skip_topics": ["sports", "politics"]
        }

        self.podcast_database = {
            "subscriptions": [
                "Lex Fridman Podcast",
                "Tim Ferriss Show",
                "Acquired"
            ],
            "recent_episodes": []
        }

        # Define tools available to the AI agent
        self.tools = [
            {
                "name": "check_user_preferences",
                "description": "Check user's interests, preferred summary length, topics to skip, and optimal delivery time. Use this FIRST to understand what the user values.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "fetch_new_episodes",
                "description": "Fetch new podcast episodes from configured RSS feeds. Returns list of episodes with metadata (title, description, duration, published date).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hours_back": {
                            "type": "number",
                            "description": "How many hours back to check for new episodes"
                        }
                    },
                    "required": ["hours_back"]
                }
            },
            {
                "name": "search_web_for_podcasts",
                "description": "Search the web for NEW podcast recommendations based on topics. Use when user wants to discover podcasts beyond their current subscriptions.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Topics to search for (e.g., ['AI safety', 'quantum computing'])"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of recommendations",
                            "default": 5
                        }
                    },
                    "required": ["topics"]
                }
            },
            {
                "name": "analyze_episode_relevance",
                "description": "Analyze if an episode is relevant to user's interests. Returns relevance score (0-1) and reasoning. Use this to filter episodes intelligently.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_title": {
                            "type": "string",
                            "description": "Episode title"
                        },
                        "episode_description": {
                            "type": "string",
                            "description": "Episode description"
                        },
                        "user_interests": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "User's interest topics"
                        }
                    },
                    "required": ["episode_title", "episode_description", "user_interests"]
                }
            },
            {
                "name": "get_transcript",
                "description": "Get transcript or content for a specific episode. Try this before summarizing.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {
                            "type": "string",
                            "description": "Episode identifier"
                        },
                        "episode_url": {
                            "type": "string",
                            "description": "Episode URL"
                        }
                    },
                    "required": ["episode_id"]
                }
            },
            {
                "name": "generate_summary",
                "description": "Generate AI-powered summary of episode. YOU decide the style based on content complexity and user's current context (busy vs free time).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {
                            "type": "string"
                        },
                        "transcript": {
                            "type": "string",
                            "description": "Episode transcript"
                        },
                        "style": {
                            "type": "string",
                            "enum": ["brief", "detailed", "technical"],
                            "description": "Summary style - choose based on: brief (user is busy), detailed (user has time), technical (complex topic needs depth)"
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific areas to focus on in the summary"
                        }
                    },
                    "required": ["episode_id", "transcript", "style"]
                }
            },
            {
                "name": "send_email_digest",
                "description": "Send email digest to user. Only use when you have valuable content to deliver.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "Email subject line"
                        },
                        "content": {
                            "type": "string",
                            "description": "Email body in markdown format"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "normal", "high"],
                            "description": "Email priority based on content value"
                        }
                    },
                    "required": ["subject", "content"]
                }
            },
            {
                "name": "save_for_later",
                "description": "Save episode to user's reading list for later review. Use when episode is valuable but not urgent.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"},
                        "reason": {
                            "type": "string",
                            "description": "Why this should be saved for later"
                        }
                    },
                    "required": ["episode_id", "reason"]
                }
            }
        ]

        # Conversation history for agentic loop
        self.conversation_history = []

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool that the AI agent chose.
        This is where AI's decisions become actions.
        """

        print(f"\n🔧 Executing tool: {tool_name}")
        print(f"   Input: {json.dumps(tool_input, indent=2)[:200]}")

        # Tool implementations
        if tool_name == "check_user_preferences":
            return {
                "success": True,
                "preferences": self.user_preferences,
                "message": "User preferences loaded"
            }

        elif tool_name == "fetch_new_episodes":
            hours_back = tool_input["hours_back"]

            # Mock episode data (in production, this would call actual RSS fetcher)
            episodes = [
                {
                    "id": "ep_001",
                    "podcast": "Lex Fridman Podcast",
                    "title": "Yann LeCun: AI Safety, Deep Learning, and the Future of AI",
                    "description": "Yann LeCun discusses AI safety concerns, the limitations of current LLMs, and why he believes AGI is still far away. Deep dive into self-supervised learning and world models.",
                    "url": "https://example.com/lex-yann-lecun",
                    "duration": "3h 15m",
                    "published": "2024-01-03"
                },
                {
                    "id": "ep_002",
                    "podcast": "Tim Ferriss Show",
                    "title": "Master Chef Gordon Ramsay on Cooking Techniques",
                    "description": "Gordon Ramsay shares his favorite recipes and cooking tips for home chefs.",
                    "url": "https://example.com/tim-gordon",
                    "duration": "2h 10m",
                    "published": "2024-01-03"
                },
                {
                    "id": "ep_003",
                    "podcast": "Acquired",
                    "title": "NVIDIA: The AI Chip Wars",
                    "description": "Deep dive into NVIDIA's dominance in AI chips, Jensen Huang's strategy, and the competitive landscape with AMD and startups.",
                    "url": "https://example.com/acquired-nvidia",
                    "duration": "4h 30m",
                    "published": "2024-01-02"
                }
            ]

            return {
                "success": True,
                "count": len(episodes),
                "episodes": episodes
            }

        elif tool_name == "search_web_for_podcasts":
            topics = tool_input["topics"]
            limit = tool_input.get("limit", 5)

            # Mock search results
            recommendations = [
                {
                    "name": "The Robot Brains Podcast",
                    "description": f"Interviews with AI researchers about {', '.join(topics)}",
                    "rss_url": "https://example.com/robot-brains/feed",
                    "relevance_score": 0.92
                }
            ]

            return {
                "success": True,
                "recommendations": recommendations
            }

        elif tool_name == "analyze_episode_relevance":
            title = tool_input["episode_title"]
            description = tool_input["episode_description"]
            interests = tool_input["user_interests"]

            # Simple relevance scoring (in production, could use embeddings)
            relevance_score = 0.5
            for interest in interests:
                if interest.lower() in title.lower() or interest.lower() in description.lower():
                    relevance_score += 0.15

            relevance_score = min(relevance_score, 1.0)

            return {
                "success": True,
                "relevance_score": relevance_score,
                "reasoning": f"Episode matches {len([i for i in interests if i.lower() in title.lower() or i.lower() in description.lower()])} of user's interests",
                "recommendation": "summarize" if relevance_score > 0.6 else "skip"
            }

        elif tool_name == "get_transcript":
            episode_id = tool_input["episode_id"]

            # Mock transcript
            transcripts = {
                "ep_001": "Lex: Welcome Yann LeCun. Let's talk about AI safety...\nYann: Thanks for having me. I think the current panic about AI existential risk is overblown...\n[Full transcript would be much longer]",
                "ep_002": "Tim: Gordon Ramsay is here. Gordon: Hello Tim, let's talk about cooking...",
                "ep_003": "Ben: Today we're diving into NVIDIA...\nDavid: Jensen Huang has built an incredible company..."
            }

            transcript = transcripts.get(episode_id, "Transcript not available")

            return {
                "success": True,
                "transcript": transcript,
                "length": len(transcript)
            }

        elif tool_name == "generate_summary":
            episode_id = tool_input["episode_id"]
            style = tool_input["style"]
            focus_areas = tool_input.get("focus_areas", [])

            # Mock summary (in production, would call actual summarizer)
            summaries = {
                "ep_001": {
                    "brief": "Yann LeCun discusses why he thinks AI safety concerns are overblown and explains his vision for future AI systems based on world models.",
                    "detailed": """## Overview
Yann LeCun, Chief AI Scientist at Meta, shares his contrarian views on AI safety and the path to AGI.

## Key Points
- Current LLMs are limited - they lack true understanding and can't plan
- AI safety panic is premature; we're far from human-level AI
- Self-supervised learning + world models are the key to next-gen AI
- Open source AI development is crucial for safety and democracy

## Highlights
- "The idea that LLMs will lead to AGI is like thinking taller ladders will get you to the moon"
- Discussion of JEPA (Joint Embedding Predictive Architecture)

## Takeaways
- Focus on building AI that understands the world through prediction
- Open collaboration beats closed development for safety""",
                    "technical": "[Technical deep-dive version with architecture details, mathematical concepts, etc.]"
                }
            }

            summary = summaries.get(episode_id, {}).get(style, "Summary not available")

            return {
                "success": True,
                "summary": summary,
                "style_used": style
            }

        elif tool_name == "send_email_digest":
            subject = tool_input["subject"]
            content = tool_input["content"]
            priority = tool_input.get("priority", "normal")

            print(f"\n📧 EMAIL WOULD BE SENT:")
            print(f"   Subject: {subject}")
            print(f"   Priority: {priority}")
            print(f"   Content preview: {content[:200]}...")

            return {
                "success": True,
                "message": "Email sent successfully",
                "sent_at": datetime.now().isoformat()
            }

        elif tool_name == "save_for_later":
            episode_id = tool_input["episode_id"]
            reason = tool_input["reason"]

            print(f"\n💾 SAVED FOR LATER: {episode_id}")
            print(f"   Reason: {reason}")

            return {
                "success": True,
                "message": f"Episode {episode_id} saved to reading list"
            }

        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

    def run_agentic_workflow(self, user_goal: str, max_iterations: int = 15) -> str:
        """
        Main agentic loop where AI makes autonomous decisions.

        This is the CORE of what makes this an AGENT:
        - AI decides what to do next (not hardcoded)
        - AI adapts based on results
        - AI works toward the goal autonomously

        Args:
            user_goal: What the user wants to achieve
            max_iterations: Max steps to prevent infinite loops

        Returns:
            Final response from the agent
        """

        print("=" * 80)
        print("🤖 AGENTIC PODCAST SUMMARIZER")
        print("=" * 80)
        print(f"\n📋 User Goal: {user_goal}\n")
        print("This is an AGENT because:")
        print("  ✓ AI decides which tools to use")
        print("  ✓ AI adapts based on results")
        print("  ✓ AI works autonomously toward the goal")
        print("  ✓ No fixed script - dynamic decision-making")
        print("=" * 80)

        # Initial system prompt that gives the AI agency
        messages = [
            {
                "role": "user",
                "content": f"""You are an intelligent, autonomous podcast research agent.

Your goal: {user_goal}

You have access to tools to help achieve this goal. Think strategically:

1. ALWAYS start by checking user preferences to understand what they value
2. Decide if you should fetch recent episodes or search for new podcasts
3. Intelligently filter episodes - don't waste time on irrelevant content
4. Choose appropriate summary styles based on:
   - Content complexity (technical topics need detailed summaries)
   - User's current context (if they mention being busy, use brief)
   - Content type (interviews vs tutorials need different approaches)
5. Only send email when you have genuinely valuable content
6. Use save_for_later for good but not urgent content

Think step-by-step. Explain your reasoning before each tool use.
You are an AGENT - make smart decisions autonomously."""
            }
        ]

        iteration = 0

        # AGENTIC LOOP - AI is in control
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'─' * 80}")
            print(f"ITERATION {iteration}")
            print(f"{'─' * 80}")

            # AI decides next action
            response = self.client.messages.create(
                model="claude-sonnet-4",
                max_tokens=4096,
                tools=self.tools,
                messages=messages
            )

            # Process AI's response
            if response.stop_reason == "tool_use":
                # AI decided to use a tool
                assistant_text = ""
                tool_use_block = None

                # Extract reasoning and tool use
                for block in response.content:
                    if block.type == "text":
                        assistant_text += block.text
                        print(f"\n💭 AI Reasoning:\n{block.text}")
                    elif block.type == "tool_use":
                        tool_use_block = block

                if tool_use_block:
                    # Execute the tool AI chose
                    tool_result = self.execute_tool(
                        tool_use_block.name,
                        tool_use_block.input
                    )

                    print(f"   ✓ Result: {json.dumps(tool_result, indent=2)[:300]}...")

                    # Update conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })

                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_block.id,
                                "content": json.dumps(tool_result)
                            }
                        ]
                    })

            elif response.stop_reason == "end_turn":
                # AI is done - goal achieved
                final_text = ""
                for block in response.content:
                    if block.type == "text":
                        final_text += block.text

                print(f"\n{'=' * 80}")
                print("✅ AGENT COMPLETED TASK")
                print(f"{'=' * 80}")
                print(f"\n{final_text}\n")
                print(f"Total iterations: {iteration}")
                print(f"{'=' * 80}")

                return final_text

            else:
                print(f"\n⚠️ Unexpected stop reason: {response.stop_reason}")
                break

        print(f"\n⚠️ Reached max iterations ({max_iterations})")
        return "Task incomplete - max iterations reached"


def main():
    """Demonstrate agentic behavior with different scenarios."""

    agent = AgenticPodcastSummarizer()

    print("\n" + "=" * 80)
    print("DEMONSTRATION: AGENTIC vs NON-AGENTIC")
    print("=" * 80)

    print("""
NON-AGENTIC (original podcast-summarizer):
  def main():
      episodes = fetch_episodes(24)      # Always fetch
      for ep in episodes:                 # Always process all
          transcript = get_transcript(ep) # Always same steps
          summary = summarize(transcript) # Always same style
      send_email(summaries)               # Always send

  Result: Fixed pipeline, no intelligence

AGENTIC (this version):
  The AI DECIDES:
  - Should I check user preferences first?
  - Which episodes actually matter to this user?
  - What summary style fits this context?
  - Is this worth sending or should I save for later?
  - Do I need to search for new podcasts?

  Result: Intelligent, context-aware behavior
    """)

    input("\nPress Enter to see the agent in action...")

    # Scenario 1: Smart filtering and prioritization
    print("\n\n" + "🎯" * 40)
    print("SCENARIO 1: User is busy, wants only high-value content")
    print("🎯" * 40)

    agent.run_agentic_workflow(
        "I'm extremely busy this week. Only send me podcast insights if there's "
        "something genuinely important about AI or technology. Skip everything else. "
        "Keep summaries brief."
    )

    input("\n\nPress Enter for next scenario...")

    # Scenario 2: Discovery mode
    print("\n\n" + "🔍" * 40)
    print("SCENARIO 2: Discovery - finding new podcasts")
    print("🔍" * 40)

    agent.run_agentic_workflow(
        "I've been listening to tech podcasts but want to explore AI safety and "
        "ethics more deeply. Find me relevant episodes or suggest new podcasts "
        "in this space. Give me detailed summaries since I have time this weekend."
    )


if __name__ == "__main__":
    main()
