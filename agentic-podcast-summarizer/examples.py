#!/usr/bin/env python3
"""
Usage Examples for Agentic Podcast Summarizer

This file demonstrates different scenarios showing how the agent
makes intelligent decisions vs a non-agentic system.
"""

from agentic_agent import AgenticPodcastSummarizer


def example_1_busy_user():
    """
    Example 1: User is busy - agent filters aggressively

    AGENTIC BEHAVIOR:
    - Checks user preferences to understand what's important
    - Analyzes each episode for relevance
    - Skips low-value content
    - Uses brief summary style (user is busy)
    - Only sends email if genuinely valuable content found
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: BUSY USER - INTELLIGENT FILTERING")
    print("=" * 80)
    print("\nScenario: User has limited time, wants only high-value content\n")

    agent = AgenticPodcastSummarizer()

    agent.run_agentic_workflow(
        "I'm extremely busy this week with a major project deadline. "
        "Only send me podcast insights if there's something genuinely "
        "important about AI or productivity. Skip everything else and "
        "keep summaries very brief."
    )

    print("\n📊 What the agent did differently than non-agentic:")
    print("  ✓ Checked preferences to understand 'important' = AI + productivity")
    print("  ✓ Analyzed each episode's relevance score")
    print("  ✓ Skipped low-relevance episodes (cooking, sports)")
    print("  ✓ Chose 'brief' summary style automatically")
    print("  ✓ Decided whether to send or save for later")
    print("\n  Non-agentic would: Process all episodes, same style, always send")


def example_2_discovery_mode():
    """
    Example 2: Discovery - agent proactively searches for new content

    AGENTIC BEHAVIOR:
    - Checks if current subscriptions have desired content
    - If insufficient, searches web for new podcasts
    - Prioritizes based on topic specificity
    - Chooses detailed summary style (user has time)
    - Provides recommendations for new subscriptions
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: DISCOVERY MODE - PROACTIVE SEARCH")
    print("=" * 80)
    print("\nScenario: User wants to explore new topics\n")

    agent = AgenticPodcastSummarizer()

    agent.run_agentic_workflow(
        "I've been listening to general tech podcasts but I want to go deeper "
        "into AI safety and ethics. Find me relevant episodes from my current "
        "podcasts, or suggest new ones I should subscribe to. I have time this "
        "weekend for long-form content."
    )

    print("\n📊 What the agent did differently:")
    print("  ✓ Identified specific topic: AI safety (not just 'AI')")
    print("  ✓ Searched current subscriptions first")
    print("  ✓ Proactively searched web for specialized podcasts")
    print("  ✓ Chose 'detailed' or 'technical' style (user has time)")
    print("  ✓ Provided recommendations for new subscriptions")
    print("\n  Non-agentic would: Only check current feeds, same processing")


def example_3_adaptive_summarization():
    """
    Example 3: Adaptive summarization based on content type

    AGENTIC BEHAVIOR:
    - Different summary styles for different content types
    - Technical papers → technical summary
    - Interviews → detailed with highlights
    - News roundups → brief summary
    - AI decides which style fits each episode
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: ADAPTIVE SUMMARIZATION")
    print("=" * 80)
    print("\nScenario: Mixed content types need different treatment\n")

    agent = AgenticPodcastSummarizer()

    agent.run_agentic_workflow(
        "Summarize the latest tech podcast episodes for me. "
        "I want to stay updated on what's happening."
    )

    print("\n📊 How the agent adapts to content:")
    print("  Episode Type              →  Summary Style Chosen")
    print("  " + "-" * 60)
    print("  Deep learning paper       →  Technical (detailed concepts)")
    print("  Founder interview         →  Detailed (story + insights)")
    print("  Weekly news roundup       →  Brief (just the headlines)")
    print("\n  Non-agentic would: Same style for everything")


def example_4_intelligent_prioritization():
    """
    Example 4: Prioritization when multiple valuable episodes exist

    AGENTIC BEHAVIOR:
    - Ranks episodes by relevance to user interests
    - Considers recency and topic overlap
    - Decides optimal number to summarize
    - May save less urgent content for later
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: INTELLIGENT PRIORITIZATION")
    print("=" * 80)
    print("\nScenario: Multiple good episodes, agent must prioritize\n")

    agent = AgenticPodcastSummarizer()

    agent.run_agentic_workflow(
        "There's been a lot of podcast activity this week. "
        "Help me catch up on the most important stuff about AI and startups."
    )

    print("\n📊 How the agent prioritizes:")
    print("  Relevance Score  Topic Overlap  Recency  →  Decision")
    print("  " + "-" * 70)
    print("  0.95             AI + startups  1 day    →  Summarize (high priority)")
    print("  0.85             AI only        2 days   →  Summarize (medium priority)")
    print("  0.70             Startups only  1 day    →  Save for later")
    print("  0.40             Cooking        1 day    →  Skip")
    print("\n  Non-agentic would: Process all or first N, no intelligence")


def example_5_context_switching():
    """
    Example 5: Agent maintains context and can switch strategies

    AGENTIC BEHAVIOR:
    - Remembers previous actions in the workflow
    - Can switch strategy mid-execution
    - Example: If few relevant episodes found, searches for more
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: ADAPTIVE STRATEGY SWITCHING")
    print("=" * 80)
    print("\nScenario: Agent adapts strategy based on findings\n")

    agent = AgenticPodcastSummarizer()

    agent.run_agentic_workflow(
        "I'm interested in quantum computing podcasts. "
        "Get me some good content on this topic."
    )

    print("\n📊 Agent's adaptive reasoning:")
    print("  Iteration 1: Check current subscriptions")
    print("  Result: Only 1 quantum computing episode found")
    print("  ")
    print("  Iteration 2: Agent thinks 'Not enough content, should search'")
    print("  Action: search_web_for_podcasts(topics=['quantum computing'])")
    print("  ")
    print("  Iteration 3: Found 3 new podcast recommendations")
    print("  Action: Provide recommendations + summarize the 1 existing episode")
    print("\n  Non-agentic would: Return the 1 episode, never search for more")


def show_architecture_explanation():
    """Show visual explanation of agentic vs non-agentic architecture."""
    print("\n" + "=" * 80)
    print("ARCHITECTURE COMPARISON")
    print("=" * 80)

    print("""
NON-AGENTIC ARCHITECTURE (Original podcast-summarizer):
┌─────────────────────────────────────────────────────────┐
│              main.py (YOU control the flow)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  def main():                                            │
│      episodes = fetch_episodes(24)        # Always 24h │
│      for ep in episodes:                  # All        │
│          transcript = get_transcript(ep)  # All        │
│          summary = summarize(transcript)  # Same       │
│      send_email(summaries)                # Always     │
│                                                         │
└─────────────────────────────────────────────────────────┘
Decision Maker: YOU (the programmer)


AGENTIC ARCHITECTURE (This project):
┌─────────────────────────────────────────────────────────┐
│          AI Agent (Claude - makes decisions)            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Agent's reasoning:                                     │
│  "User is busy → check preferences first"              │
│  "User likes AI → filter for AI topics"               │
│  "Low relevance episodes → skip them"                  │
│  "User needs brief summaries → use brief style"       │
│  "Only 1 good episode → not worth email, save later"  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Agent selects tools dynamically:                       │
│  → check_user_preferences()                            │
│  → fetch_episodes(hours_back=?)  // AI decides hours  │
│  → analyze_relevance(episode)    // AI decides filter │
│  → generate_summary(style=?)     // AI picks style    │
│  → save_for_later()              // AI decides action │
│                                                         │
└─────────────────────────────────────────────────────────┘
Decision Maker: THE AI (Claude Sonnet 4)
""")


def main():
    """Run all examples to demonstrate agentic behavior."""

    print("\n" + "🤖" * 40)
    print("AGENTIC PODCAST SUMMARIZER - USAGE EXAMPLES")
    print("🤖" * 40)

    print("""
This file demonstrates the KEY DIFFERENCE between agentic and non-agentic systems.

AGENTIC = AI makes decisions based on context
NON-AGENTIC = Programmer writes fixed logic

Watch how the agent ADAPTS to different scenarios...
""")

    input("Press Enter to start examples...")

    # Show architecture first
    show_architecture_explanation()
    input("\n\nPress Enter to continue to examples...")

    # Run examples
    example_1_busy_user()
    input("\n\nPress Enter for next example...")

    example_2_discovery_mode()
    input("\n\nPress Enter for next example...")

    example_3_adaptive_summarization()
    input("\n\nPress Enter for next example...")

    example_4_intelligent_prioritization()
    input("\n\nPress Enter for next example...")

    example_5_context_switching()

    # Final summary
    print("\n" + "=" * 80)
    print("🎓 KEY LEARNING")
    print("=" * 80)
    print("""
The difference between AGENTIC and NON-AGENTIC is NOT about:
  ❌ Having AI (you can use AI in non-agentic systems for summarization)
  ❌ Being automated (non-agentic systems can be automated too)
  ❌ Being complex (agents can be simple!)

The difference IS about WHO MAKES DECISIONS:
  ✓ Agentic: AI decides what to do based on context and goals
  ✓ Non-agentic: Programmer hardcodes what to do in all situations

In this project:
  • Same tools (fetch, summarize, email)
  • Different control: AI orchestrator vs scripted pipeline
  • Result: Intelligent, adaptive behavior vs fixed execution

This is OPTION 1: Simple Agentic Upgrade
  → Next: Multi-agent system (Option 2)
  → Then: MCP-based architecture (Option 3)
""")


if __name__ == "__main__":
    main()
