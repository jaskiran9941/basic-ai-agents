#!/usr/bin/env python3
"""
Streamlit UI for Agentic Podcast Summarizer
OpenAI GPT-4 Implementation
"""

import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Page config
st.set_page_config(
    page_title="Agentic Podcast Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)


class OpenAIAgenticAgent:
    """Agentic agent using OpenAI GPT-4 with tool calling."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"

        # Mock user preferences
        self.user_preferences = {
            "recent_topics": ["AI", "productivity", "technology"],
            "preferred_length": "detailed",
            "skip_topics": ["sports", "politics"]
        }

        # Define tools in OpenAI format
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "check_user_preferences",
                    "description": "Check user's interests, preferred summary length, and topics to skip",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_new_episodes",
                    "description": "Fetch new podcast episodes from RSS feeds",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "hours_back": {
                                "type": "number",
                                "description": "How many hours back to check for episodes"
                            }
                        },
                        "required": ["hours_back"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_episode_relevance",
                    "description": "Analyze if an episode is relevant to user's interests (returns relevance score 0-1)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "episode_title": {"type": "string"},
                            "user_interests": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["episode_title", "user_interests"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_summary",
                    "description": "Generate AI summary with chosen style: brief (user is busy), detailed (user has time), or technical (complex topics)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "episode_id": {"type": "string"},
                            "style": {
                                "type": "string",
                                "enum": ["brief", "detailed", "technical"],
                                "description": "Summary style - choose based on context"
                            }
                        },
                        "required": ["episode_id", "style"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_email_digest",
                    "description": "Send email digest to user (only use when you have valuable content)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["subject", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_for_later",
                    "description": "Save episode to reading list for later (use when content is good but not urgent)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "episode_id": {"type": "string"},
                            "reason": {"type": "string"}
                        },
                        "required": ["episode_id", "reason"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_args: Dict) -> Dict:
        """Execute the tool that AI chose."""

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
                    "description": "Yann LeCun discusses AI safety, limitations of LLMs, and path to AGI.",
                    "duration": "3h 15m",
                    "published": "2024-01-03"
                },
                {
                    "id": "ep_002",
                    "podcast": "Tim Ferriss Show",
                    "title": "Gordon Ramsay on Cooking Techniques",
                    "description": "Gordon shares cooking tips.",
                    "duration": "2h 10m",
                    "published": "2024-01-03"
                },
                {
                    "id": "ep_003",
                    "podcast": "Acquired",
                    "title": "NVIDIA: The AI Chip Wars",
                    "description": "Deep dive into NVIDIA's AI chip dominance.",
                    "duration": "4h 30m",
                    "published": "2024-01-02"
                }
            ]
            return {"success": True, "episodes": episodes, "count": len(episodes)}

        elif tool_name == "analyze_episode_relevance":
            title = tool_args.get("episode_title", "")
            interests = tool_args.get("user_interests", [])

            score = 0.5
            matches = 0
            for interest in interests:
                if interest.lower() in title.lower():
                    score += 0.15
                    matches += 1

            score = min(score, 1.0)

            return {
                "success": True,
                "relevance_score": round(score, 2),
                "matches": matches,
                "reasoning": f"Episode matches {matches} of user's {len(interests)} interests",
                "recommendation": "summarize" if score > 0.6 else "skip"
            }

        elif tool_name == "generate_summary":
            style = tool_args.get("style", "detailed")
            episode_id = tool_args.get("episode_id")

            summaries = {
                "ep_001": f"[{style.upper()} SUMMARY] Yann LeCun, Meta's Chief AI Scientist, challenges mainstream AI safety narratives. Key points: Current LLMs lack true understanding, AI existential risk concerns are overblown, self-supervised learning + world models are the path forward.",
                "ep_002": f"[{style.upper()} SUMMARY] Gordon Ramsay shares professional cooking techniques for home chefs.",
                "ep_003": f"[{style.upper()} SUMMARY] Deep analysis of NVIDIA's dominance in AI chip market, Jensen Huang's strategy, and competitive landscape."
            }

            return {
                "success": True,
                "summary": summaries.get(episode_id, f"Summary for {episode_id}"),
                "style_used": style
            }

        elif tool_name == "send_email_digest":
            return {
                "success": True,
                "message": "Email sent successfully",
                "sent_at": datetime.now().isoformat()
            }

        elif tool_name == "save_for_later":
            return {
                "success": True,
                "message": f"Saved episode {tool_args.get('episode_id')} for later"
            }

        return {"error": f"Unknown tool: {tool_name}"}

    def run_with_visualization(self, user_goal: str, max_iterations: int = 10):
        """Run agent with Streamlit visualization."""

        messages = [{
            "role": "user",
            "content": f"""You are an intelligent, autonomous podcast research agent.

Your goal: {user_goal}

Think strategically and explain your reasoning clearly before each action.

Guidelines:
1. ALWAYS start by checking user preferences to understand what they value
2. Intelligently filter episodes based on relevance - don't process irrelevant content
3. Choose appropriate summary styles:
   - 'brief' if user is busy or content is straightforward
   - 'detailed' if user has time or content is valuable
   - 'technical' if content is complex or highly technical
4. Only send email when you have genuinely valuable content
5. Use save_for_later for good but not urgent content

Work autonomously toward the goal. Explain your decisions."""
        }]

        # Visualization containers
        progress_bar = st.progress(0)
        status_text = st.empty()

        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            progress_bar.progress(min(iteration / max_iterations, 1.0))
            status_text.markdown(f"**Iteration {iteration}/{max_iterations}**")

            # Create iteration section
            with st.expander(f"🔄 Iteration {iteration}", expanded=(iteration <= 3)):
                # Call OpenAI
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto"
                )

                choice = response.choices[0]
                message = choice.message
                finish_reason = choice.finish_reason

                # Show AI reasoning
                if message.content:
                    st.markdown("### 💭 AI Reasoning")
                    st.markdown(
                        f'<div class="reasoning-box">{message.content}</div>',
                        unsafe_allow_html=True
                    )

                # Handle tool calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        st.markdown(f"### 🔧 Tool: **{tool_call.function.name}**")

                        # Parse arguments
                        tool_args = json.loads(tool_call.function.arguments)

                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown("**Input:**")
                        with col2:
                            st.json(tool_args)

                        # Execute tool
                        result = self.execute_tool(tool_call.function.name, tool_args)

                        st.markdown("### ✅ Result")
                        st.markdown(
                            f'<div class="result-box">{json.dumps(result, indent=2)}</div>',
                            unsafe_allow_html=True
                        )

                        # Update conversation
                        messages.append({
                            "role": "assistant",
                            "content": message.content,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_call.function.name,
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]
                        })

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })

                # Check if done
                elif finish_reason == "stop":
                    st.markdown("### 🎯 Agent Completed")
                    st.success(message.content or "Task complete!")
                    progress_bar.progress(1.0)
                    status_text.markdown("**✅ Complete!**")
                    return message.content

        st.warning(f"Reached max iterations ({max_iterations})")
        return "Task incomplete"


def main():
    """Main Streamlit app."""

    st.title("🤖 Agentic Podcast Summarizer")
    st.markdown("### Powered by OpenAI GPT-4")

    # Sidebar
    with st.sidebar:
        st.header("🔑 Configuration")

        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Get from platform.openai.com"
        )

        st.divider()

        st.header("📋 Why It's Agentic")
        st.markdown("""
        ✅ **AI decides** what to do
        ✅ **Adapts** to context
        ✅ **Reasons** before acting
        ✅ **Chooses** tools dynamically
        ✅ **Works toward** goals autonomously

        Watch the AI think! 🧠
        """)

        st.divider()

        st.header("🎯 Quick Presets")
        if st.button("📌 Busy User"):
            st.session_state.preset = "busy"
        if st.button("🔍 Discovery"):
            st.session_state.preset = "discovery"
        if st.button("🎓 Deep Dive"):
            st.session_state.preset = "deep"

    # Main area
    tab1, tab2 = st.tabs(["🤖 Run Agent", "❓ What Makes It Agentic?"])

    with tab1:
        st.markdown("## Run the Agentic Workflow")

        # Goal presets
        preset = st.session_state.get('preset', None)
        if preset == "busy":
            default_goal = "I'm extremely busy this week. Only send me insights if there's something genuinely important about AI. Keep it brief."
        elif preset == "discovery":
            default_goal = "I want to learn about AI safety. Find relevant content from my podcasts or suggest new ones."
        elif preset == "deep":
            default_goal = "I have time this weekend for deep technical content about AI. Give me detailed summaries."
        else:
            default_goal = "Get me valuable podcast insights from the last 24 hours."

        user_goal = st.text_area(
            "What should the agent do?",
            value=default_goal,
            height=100
        )

        max_iterations = st.slider("Max iterations", 5, 15, 8)

        if st.button("🚀 Run Agent", type="primary", disabled=not api_key):
            if not api_key:
                st.error("⚠️ Please enter your OpenAI API key in the sidebar")
            else:
                st.markdown("---")
                st.info("🔄 Agent is working... Watch the decisions unfold!")

                agent = OpenAIAgenticAgent(api_key)

                try:
                    result = agent.run_with_visualization(user_goal, max_iterations)
                    st.markdown("---")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())

    with tab2:
        st.markdown("## ❓ What Makes This Agentic?")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ❌ Non-Agentic")
            st.code("""
# YOU decide everything
episodes = fetch_all()
for ep in episodes:
    summary = summarize(ep)
send_email(summaries)
            """)
            st.error("Fixed pipeline, no intelligence")

        with col2:
            st.markdown("### ✅ Agentic")
            st.code("""
# AI decides everything
agent = AIAgent(
    goal="Get insights"
)
agent.run()  # Autonomous!
            """)
            st.success("Intelligent, adaptive")

        st.markdown("---")

        st.markdown("### The 5 Characteristics")

        with st.expander("1️⃣ Autonomous Decision-Making"):
            st.markdown("""
            **AI chooses** actions based on context.

            Example: User says "I'm busy" → AI decides to use 'brief' summaries
            """)

        with st.expander("2️⃣ Goal-Oriented Behavior"):
            st.markdown("""
            **Works toward objectives**, not just steps.

            Example: Goal = "Find AI safety content" → AI searches current podcasts,
            then searches web for new ones if needed
            """)

        with st.expander("3️⃣ Dynamic Tool Selection"):
            st.markdown("""
            **Picks tools** based on situation.

            Different scenarios = different tools chosen
            """)

        with st.expander("4️⃣ Planning & Reasoning"):
            st.markdown("""
            **Thinks** before acting.

            Watch the "AI Reasoning" boxes - you'll see it plan!
            """)

        with st.expander("5️⃣ Adaptive Behavior"):
            st.markdown("""
            **Observes results** and adjusts.

            Example: Only 1 relevant episode found → AI searches for more
            """)


if __name__ == "__main__":
    main()
