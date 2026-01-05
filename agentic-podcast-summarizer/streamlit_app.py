#!/usr/bin/env python3
"""
Streamlit UI for Agentic Podcast Summarizer

This UI visualizes the agent's decision-making process in real-time.
You can see:
- Agent's reasoning at each step
- Which tools it chooses and why
- How it adapts based on results
- The difference between agentic and non-agentic behavior
"""

import streamlit as st
from anthropic import Anthropic
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


# Page config
st.set_page_config(
    page_title="Agentic Podcast Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visualization
st.markdown("""
<style>
    .reasoning-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
    }
    .tool-call-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 10px 0;
    }
    .result-box {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 10px 0;
    }
    .agent-decision {
        font-weight: bold;
        color: #4CAF50;
    }
    .comparison-table {
        width: 100%;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitAgenticAgent:
    """
    Agentic agent with Streamlit visualization.
    Shows real-time decision-making process.
    """

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.iteration_count = 0

        # Mock data
        self.user_preferences = {
            "recent_topics": ["AI", "productivity", "technology"],
            "preferred_length": "detailed",
            "active_time": "morning",
            "skip_topics": ["sports", "politics"]
        }

        # Define tools
        self.tools = [
            {
                "name": "check_user_preferences",
                "description": "Check user's interests, preferred summary length, topics to skip, and optimal delivery time.",
                "input_schema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "fetch_new_episodes",
                "description": "Fetch new podcast episodes from configured RSS feeds.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hours_back": {"type": "number", "description": "Hours back to check"}
                    },
                    "required": ["hours_back"]
                }
            },
            {
                "name": "search_web_for_podcasts",
                "description": "Search web for new podcast recommendations.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topics": {"type": "array", "items": {"type": "string"}},
                        "limit": {"type": "number", "default": 5}
                    },
                    "required": ["topics"]
                }
            },
            {
                "name": "analyze_episode_relevance",
                "description": "Analyze episode relevance to user interests (returns score 0-1).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_title": {"type": "string"},
                        "episode_description": {"type": "string"},
                        "user_interests": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["episode_title", "episode_description", "user_interests"]
                }
            },
            {
                "name": "get_transcript",
                "description": "Get transcript for an episode.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"}
                    },
                    "required": ["episode_id"]
                }
            },
            {
                "name": "generate_summary",
                "description": "Generate summary with chosen style (brief/detailed/technical).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"},
                        "transcript": {"type": "string"},
                        "style": {"type": "string", "enum": ["brief", "detailed", "technical"]}
                    },
                    "required": ["episode_id", "transcript", "style"]
                }
            },
            {
                "name": "send_email_digest",
                "description": "Send email digest to user.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["subject", "content"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict) -> Dict:
        """Execute tool and return result."""

        if tool_name == "check_user_preferences":
            return {
                "success": True,
                "preferences": self.user_preferences
            }

        elif tool_name == "fetch_new_episodes":
            episodes = [
                {
                    "id": "ep_001",
                    "podcast": "Lex Fridman Podcast",
                    "title": "Yann LeCun: AI Safety, Deep Learning, and the Future of AI",
                    "description": "Yann LeCun discusses AI safety concerns, limitations of LLMs, and the path to AGI through self-supervised learning.",
                    "duration": "3h 15m",
                    "published": "2024-01-03"
                },
                {
                    "id": "ep_002",
                    "podcast": "Tim Ferriss Show",
                    "title": "Master Chef Gordon Ramsay on Cooking Techniques",
                    "description": "Gordon Ramsay shares cooking tips and recipes.",
                    "duration": "2h 10m",
                    "published": "2024-01-03"
                },
                {
                    "id": "ep_003",
                    "podcast": "Acquired",
                    "title": "NVIDIA: The AI Chip Wars",
                    "description": "Deep dive into NVIDIA's dominance in AI chips and competitive landscape.",
                    "duration": "4h 30m",
                    "published": "2024-01-02"
                }
            ]
            return {"success": True, "count": len(episodes), "episodes": episodes}

        elif tool_name == "search_web_for_podcasts":
            return {
                "success": True,
                "recommendations": [
                    {
                        "name": "The Robot Brains Podcast",
                        "description": "Interviews with AI researchers",
                        "relevance_score": 0.92
                    }
                ]
            }

        elif tool_name == "analyze_episode_relevance":
            title = tool_input["episode_title"]
            interests = tool_input["user_interests"]

            score = 0.5
            for interest in interests:
                if interest.lower() in title.lower():
                    score += 0.15

            score = min(score, 1.0)

            return {
                "success": True,
                "relevance_score": score,
                "reasoning": f"Matches {len([i for i in interests if i.lower() in title.lower()])} user interests",
                "recommendation": "summarize" if score > 0.6 else "skip"
            }

        elif tool_name == "get_transcript":
            return {
                "success": True,
                "transcript": "Sample transcript content...",
                "length": 5000
            }

        elif tool_name == "generate_summary":
            style = tool_input["style"]
            return {
                "success": True,
                "summary": f"Generated {style} summary of the episode...",
                "style_used": style
            }

        elif tool_name == "send_email_digest":
            return {
                "success": True,
                "message": "Email sent successfully",
                "sent_at": datetime.now().isoformat()
            }

        return {"success": False, "error": f"Unknown tool: {tool_name}"}

    def run_with_visualization(self, user_goal: str, max_iterations: int = 10):
        """
        Run agent with real-time Streamlit visualization.
        """

        messages = [
            {
                "role": "user",
                "content": f"""You are an intelligent, autonomous podcast research agent.

Your goal: {user_goal}

Think strategically and explain your reasoning before each action.
ALWAYS start by checking user preferences.
Choose appropriate summary styles based on context.
Only send email when you have genuinely valuable content."""
            }
        ]

        # Create containers for visualization
        progress_container = st.container()

        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()

        # Main execution container
        execution_container = st.container()

        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            self.iteration_count = iteration

            # Update progress
            progress_bar.progress(min(iteration / max_iterations, 1.0))
            status_text.markdown(f"**Iteration {iteration}/{max_iterations}**")

            # Create iteration expander
            with execution_container:
                with st.expander(f"🔄 Iteration {iteration}", expanded=(iteration <= 3)):
                    # Call AI
                    response = self.client.messages.create(
                        model="claude-sonnet-4",
                        max_tokens=4096,
                        tools=self.tools,
                        messages=messages
                    )

                    # Process response
                    if response.stop_reason == "tool_use":
                        assistant_text = ""
                        tool_use_block = None

                        for block in response.content:
                            if block.type == "text":
                                assistant_text += block.text
                            elif block.type == "tool_use":
                                tool_use_block = block

                        # Show AI reasoning
                        if assistant_text:
                            st.markdown("### 💭 AI Reasoning")
                            st.markdown(f'<div class="reasoning-box">{assistant_text}</div>',
                                      unsafe_allow_html=True)

                        # Show tool call
                        if tool_use_block:
                            st.markdown("### 🔧 Tool Selection")

                            col1, col2 = st.columns([1, 2])

                            with col1:
                                st.markdown(f'<div class="agent-decision">Agent chose: {tool_use_block.name}</div>',
                                          unsafe_allow_html=True)

                            with col2:
                                with st.expander("View Input"):
                                    st.json(tool_use_block.input)

                            # Execute tool
                            tool_result = self.execute_tool(tool_use_block.name, tool_use_block.input)

                            # Show result
                            st.markdown("### ✅ Result")
                            st.markdown(f'<div class="result-box">{json.dumps(tool_result, indent=2)[:300]}...</div>',
                                      unsafe_allow_html=True)

                            # Update messages
                            messages.append({
                                "role": "assistant",
                                "content": response.content
                            })

                            messages.append({
                                "role": "user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_block.id,
                                    "content": json.dumps(tool_result)
                                }]
                            })

                    elif response.stop_reason == "end_turn":
                        # Agent is done
                        final_text = ""
                        for block in response.content:
                            if block.type == "text":
                                final_text += block.text

                        st.markdown("### 🎯 Agent Completed Task")
                        st.success(final_text)

                        progress_bar.progress(1.0)
                        status_text.markdown("**✅ Complete!**")

                        return final_text

                    else:
                        st.error(f"Unexpected stop reason: {response.stop_reason}")
                        break

        st.warning(f"Reached max iterations ({max_iterations})")
        return "Task incomplete"


def main():
    """Main Streamlit app."""

    # Header
    st.title("🤖 Agentic Podcast Summarizer")
    st.markdown("### Watch the AI Agent Make Autonomous Decisions")

    # Sidebar
    with st.sidebar:
        st.header("🔑 Configuration")

        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            help="Get your key from console.anthropic.com"
        )

        st.divider()

        st.header("📋 About This Agent")
        st.markdown("""
        This is an **AGENTIC** system because:

        ✅ **AI decides** what to do
        ✅ **Adapts** to context
        ✅ **Reasons** before acting
        ✅ **Chooses** tools dynamically
        ✅ **Works toward** goals

        Watch the reasoning process unfold!
        """)

        st.divider()

        st.header("🎯 Try These Goals")

        if st.button("📌 Busy User"):
            st.session_state.selected_goal = "busy"

        if st.button("🔍 Discovery Mode"):
            st.session_state.selected_goal = "discovery"

        if st.button("🎓 Deep Dive"):
            st.session_state.selected_goal = "deep_dive"

    # Main content
    tab1, tab2, tab3 = st.tabs(["🤖 Run Agent", "📊 Comparison", "❓ What Makes It Agentic?"])

    with tab1:
        st.markdown("## Run the Agentic Workflow")

        # Goal selection
        goal_preset = st.session_state.get('selected_goal', None)

        if goal_preset == "busy":
            default_goal = "I'm extremely busy this week. Only send me insights if there's something genuinely important about AI. Keep it brief."
        elif goal_preset == "discovery":
            default_goal = "I want to learn about AI safety. Find relevant content from my podcasts or suggest new ones."
        elif goal_preset == "deep_dive":
            default_goal = "I have time this weekend for deep technical content about AI and machine learning. Give me detailed summaries."
        else:
            default_goal = "Get me valuable podcast insights from the last 24 hours."

        user_goal = st.text_area(
            "What would you like the agent to do?",
            value=default_goal,
            height=100,
            help="The agent will work autonomously to achieve this goal"
        )

        max_iterations = st.slider("Max iterations", 5, 20, 10)

        if st.button("🚀 Run Agent", type="primary", disabled=not api_key):
            if not api_key:
                st.error("Please enter your Anthropic API key in the sidebar")
            else:
                st.markdown("---")
                st.markdown("### 🔄 Agent Execution")
                st.info("Watch how the AI makes decisions at each step...")

                agent = StreamlitAgenticAgent(api_key)

                try:
                    result = agent.run_with_visualization(user_goal, max_iterations)

                    st.markdown("---")
                    st.balloons()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())

    with tab2:
        st.markdown("## 📊 Agentic vs Non-Agentic Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ❌ Non-Agentic (Original)")
            st.code("""
def main():
    # YOU write control flow
    episodes = fetch_episodes(24)

    for ep in episodes:
        # Process ALL episodes
        transcript = get_transcript(ep)

        # SAME style always
        summary = summarize(transcript)

    # ALWAYS send
    send_email(summaries)
            """, language="python")

            st.error("**Fixed pipeline - no intelligence**")
            st.markdown("""
            - Processes **all** episodes
            - **Same** steps always
            - **No** filtering
            - **No** adaptation
            - **You** make decisions
            """)

        with col2:
            st.markdown("### ✅ Agentic (This Version)")
            st.code("""
def main():
    # AI writes control flow
    agent = AIAgent(
        goal="Get valuable insights"
    )

    # AI decides:
    # - Check preferences?
    # - Which episodes matter?
    # - What style to use?
    # - Send now or later?

    agent.run()  # Autonomous!
            """, language="python")

            st.success("**Intelligent decision-making**")
            st.markdown("""
            - Filters **intelligently**
            - **Adapts** to context
            - **Different** styles per episode
            - **Decides** when to send
            - **AI** makes decisions
            """)

        st.markdown("---")

        st.markdown("### Decision-Making Comparison")

        comparison_data = {
            "Aspect": ["Who decides?", "Filtering", "Summary style", "Adaptation", "Tool selection"],
            "Non-Agentic": ["Programmer", "None (process all)", "Fixed", "None", "Sequential, hardcoded"],
            "Agentic": ["AI", "Intelligent (relevance scoring)", "Dynamic (context-aware)", "Continuous", "Dynamic, situation-based"]
        }

        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

    with tab3:
        st.markdown("## ❓ What Makes This Agentic?")

        st.markdown("### The 5 Core Characteristics")

        with st.expander("1️⃣ Autonomous Decision-Making", expanded=True):
            st.markdown("""
            The AI **chooses** actions based on context, not fixed if/else logic.

            **Example:**
            ```
            User: "I'm busy this week"

            AI thinks:
            → User is busy → use 'brief' summaries
            → Check what's important to them first
            → Filter aggressively (only high relevance)
            ```

            The AI made 3 decisions autonomously!
            """)

        with st.expander("2️⃣ Goal-Oriented Behavior"):
            st.markdown("""
            Works toward **objectives**, not just executing steps.

            **Example:**
            ```
            Goal: "Find AI safety content"

            AI's approach:
            1. Check current subscriptions for AI safety
            2. If not enough → search web for new podcasts
            3. Prioritize safety-specific (not general AI)
            4. Choose detailed style (complex topic)
            ```

            The AI created a multi-step plan to achieve the goal!
            """)

        with st.expander("3️⃣ Dynamic Tool Use"):
            st.markdown("""
            Selects appropriate tools **based on situation**.

            **Different scenarios, different tools:**

            | Scenario | Tools AI Chose |
            |----------|----------------|
            | User has favorites | fetch_episodes → analyze → summarize |
            | User wants new topics | check_preferences → **search_web** → fetch |
            | Low relevance found | analyze → **save_for_later** (not email) |

            Same agent, different tool sequences!
            """)

        with st.expander("4️⃣ Planning & Reasoning"):
            st.markdown("""
            Thinks about the **best approach** before acting.

            **Watch the reasoning in the UI:**
            ```
            💭 AI Reasoning:
            "I should start by checking the user's preferences
            to understand what topics they're interested in.
            Then I'll fetch recent episodes and filter them
            based on relevance before deciding which ones
            to summarize."
            ```

            This appears in the Streamlit UI when you run the agent!
            """)

        with st.expander("5️⃣ Adaptive Behavior"):
            st.markdown("""
            **Observes results** and adjusts strategy.

            **Example adaptation:**
            ```
            Iteration 1: fetch_episodes() → 3 episodes found
            Iteration 2: analyze_relevance() → only 1 relevant
            Iteration 3: AI adapts:
                        "Not enough content, let me search
                         for more instead of sending thin email"
                        → search_web_for_podcasts()
            ```

            The AI changed its strategy mid-execution!
            """)

        st.markdown("---")
        st.info("""
        **Key Insight:** This isn't just using AI for summarization.
        The AI is **orchestrating the entire workflow** and making
        all the decisions about what to do and when.

        That's what makes it an AGENT! 🤖
        """)


if __name__ == "__main__":
    main()
