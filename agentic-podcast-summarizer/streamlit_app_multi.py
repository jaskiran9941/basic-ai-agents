#!/usr/bin/env python3
"""
Streamlit UI for Agentic Podcast Summarizer
Supports both Anthropic Claude and OpenAI GPT-4
"""

import streamlit as st
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
    .agent-decision {
        font-weight: bold;
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)


class MultiProviderAgenticAgent:
    """
    Agentic agent that supports both Anthropic and OpenAI.
    """

    def __init__(self, provider: str, api_key: str):
        self.provider = provider

        if provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-sonnet-4"
        elif provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4-turbo-preview"
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        # Mock data
        self.user_preferences = {
            "recent_topics": ["AI", "productivity", "technology"],
            "preferred_length": "detailed",
            "skip_topics": ["sports", "politics"]
        }

        # Define tools (common format works for both)
        self.tools = self._get_tools()

    def _get_tools(self):
        """Get tools in the appropriate format for the provider."""

        if self.provider == "anthropic":
            # Anthropic format
            return [
                {
                    "name": "check_user_preferences",
                    "description": "Check user's interests and preferences",
                    "input_schema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "fetch_new_episodes",
                    "description": "Fetch new podcast episodes",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "hours_back": {"type": "number", "description": "Hours to check"}
                        },
                        "required": ["hours_back"]
                    }
                },
                {
                    "name": "analyze_episode_relevance",
                    "description": "Analyze if episode matches user interests",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "episode_title": {"type": "string"},
                            "user_interests": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["episode_title", "user_interests"]
                    }
                },
                {
                    "name": "generate_summary",
                    "description": "Generate summary with style (brief/detailed/technical)",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "episode_id": {"type": "string"},
                            "style": {"type": "string", "enum": ["brief", "detailed", "technical"]}
                        },
                        "required": ["episode_id", "style"]
                    }
                },
                {
                    "name": "send_email_digest",
                    "description": "Send email with summaries",
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

        else:  # OpenAI format
            return [
                {
                    "type": "function",
                    "function": {
                        "name": "check_user_preferences",
                        "description": "Check user's interests and preferences",
                        "parameters": {"type": "object", "properties": {}}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "fetch_new_episodes",
                        "description": "Fetch new podcast episodes",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "hours_back": {"type": "number", "description": "Hours to check"}
                            },
                            "required": ["hours_back"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "analyze_episode_relevance",
                        "description": "Analyze if episode matches user interests",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "episode_title": {"type": "string"},
                                "user_interests": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["episode_title", "user_interests"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "generate_summary",
                        "description": "Generate summary with style",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "episode_id": {"type": "string"},
                                "style": {"type": "string", "enum": ["brief", "detailed", "technical"]}
                            },
                            "required": ["episode_id", "style"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "send_email_digest",
                        "description": "Send email with summaries",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "subject": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["subject", "content"]
                        }
                    }
                }
            ]

    def execute_tool(self, tool_name: str, tool_input: Dict) -> Dict:
        """Execute tool and return result."""

        if tool_name == "check_user_preferences":
            return {"success": True, "preferences": self.user_preferences}

        elif tool_name == "fetch_new_episodes":
            episodes = [
                {
                    "id": "ep_001",
                    "title": "Yann LeCun: AI Safety and Deep Learning",
                    "podcast": "Lex Fridman",
                    "relevance": "high"
                },
                {
                    "id": "ep_002",
                    "title": "Gordon Ramsay Cooking Tips",
                    "podcast": "Tim Ferriss",
                    "relevance": "low"
                }
            ]
            return {"success": True, "episodes": episodes, "count": len(episodes)}

        elif tool_name == "analyze_episode_relevance":
            title = tool_input.get("episode_title", "")
            interests = tool_input.get("user_interests", [])

            score = 0.5
            for interest in interests:
                if interest.lower() in title.lower():
                    score += 0.15

            return {
                "relevance_score": min(score, 1.0),
                "recommendation": "summarize" if score > 0.6 else "skip"
            }

        elif tool_name == "generate_summary":
            style = tool_input.get("style", "detailed")
            return {
                "success": True,
                "summary": f"Generated {style} summary...",
                "style_used": style
            }

        elif tool_name == "send_email_digest":
            return {"success": True, "sent_at": datetime.now().isoformat()}

        return {"error": f"Unknown tool: {tool_name}"}

    def run_with_visualization(self, user_goal: str, max_iterations: int = 8):
        """Run agent with Streamlit visualization."""

        if self.provider == "anthropic":
            return self._run_anthropic(user_goal, max_iterations)
        else:
            return self._run_openai(user_goal, max_iterations)

    def _run_anthropic(self, user_goal: str, max_iterations: int):
        """Run with Anthropic Claude."""

        messages = [{
            "role": "user",
            "content": f"You are an autonomous podcast agent. Goal: {user_goal}\n\nThink strategically. Explain your reasoning. ALWAYS check preferences first."
        }]

        progress_bar = st.progress(0)
        status_text = st.empty()
        execution_container = st.container()

        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            progress_bar.progress(iteration / max_iterations)
            status_text.markdown(f"**Iteration {iteration}/{max_iterations}**")

            with execution_container:
                with st.expander(f"🔄 Iteration {iteration}", expanded=(iteration <= 3)):
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=4096,
                        tools=self.tools,
                        messages=messages
                    )

                    if response.stop_reason == "tool_use":
                        assistant_text = ""
                        tool_use_block = None

                        for block in response.content:
                            if block.type == "text":
                                assistant_text += block.text
                            elif block.type == "tool_use":
                                tool_use_block = block

                        if assistant_text:
                            st.markdown("### 💭 AI Reasoning")
                            st.markdown(f'<div class="reasoning-box">{assistant_text}</div>', unsafe_allow_html=True)

                        if tool_use_block:
                            st.markdown(f"### 🔧 Tool: **{tool_use_block.name}**")
                            st.json(tool_use_block.input)

                            tool_result = self.execute_tool(tool_use_block.name, tool_use_block.input)

                            st.markdown("### ✅ Result")
                            st.json(tool_result)

                            messages.append({"role": "assistant", "content": response.content})
                            messages.append({
                                "role": "user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_block.id,
                                    "content": json.dumps(tool_result)
                                }]
                            })

                    elif response.stop_reason == "end_turn":
                        final_text = "".join(block.text for block in response.content if block.type == "text")
                        st.success(f"✅ Complete: {final_text}")
                        return final_text

        return "Max iterations reached"

    def _run_openai(self, user_goal: str, max_iterations: int):
        """Run with OpenAI GPT-4."""

        messages = [{
            "role": "user",
            "content": f"You are an autonomous podcast agent. Goal: {user_goal}\n\nThink step by step. Explain reasoning. Check preferences first."
        }]

        progress_bar = st.progress(0)
        status_text = st.empty()
        execution_container = st.container()

        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            progress_bar.progress(iteration / max_iterations)
            status_text.markdown(f"**Iteration {iteration}/{max_iterations}**")

            with execution_container:
                with st.expander(f"🔄 Iteration {iteration}", expanded=(iteration <= 3)):
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        tools=self.tools,
                        tool_choice="auto"
                    )

                    message = response.choices[0].message

                    # Show reasoning if present
                    if message.content:
                        st.markdown("### 💭 AI Reasoning")
                        st.markdown(f'<div class="reasoning-box">{message.content}</div>', unsafe_allow_html=True)

                    # Handle tool calls
                    if message.tool_calls:
                        for tool_call in message.tool_calls:
                            st.markdown(f"### 🔧 Tool: **{tool_call.function.name}**")
                            st.json(json.loads(tool_call.function.arguments))

                            tool_result = self.execute_tool(
                                tool_call.function.name,
                                json.loads(tool_call.function.arguments)
                            )

                            st.markdown("### ✅ Result")
                            st.json(tool_result)

                            messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result)
                            })

                    elif message.finish_reason == "stop":
                        st.success(f"✅ Complete: {message.content}")
                        return message.content

        return "Max iterations reached"


def main():
    """Main Streamlit app."""

    st.title("🤖 Agentic Podcast Summarizer")
    st.markdown("### Multi-Provider Support: Anthropic Claude & OpenAI GPT-4")

    # Sidebar
    with st.sidebar:
        st.header("🔑 Configuration")

        provider = st.radio(
            "Choose AI Provider",
            ["anthropic", "openai"],
            format_func=lambda x: "Anthropic Claude" if x == "anthropic" else "OpenAI GPT-4"
        )

        if provider == "anthropic":
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                value=os.getenv("ANTHROPIC_API_KEY", ""),
                help="Get from console.anthropic.com"
            )
        else:
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=os.getenv("OPENAI_API_KEY", ""),
                help="Get from platform.openai.com"
            )

        st.divider()
        st.markdown("""
        **Why it's agentic:**
        ✅ AI decides what to do
        ✅ Adapts to context
        ✅ Chooses tools dynamically
        ✅ Works toward goals
        """)

    # Main area
    st.markdown("## Run the Agent")

    user_goal = st.text_area(
        "What should the agent do?",
        value="I'm busy this week. Only send important AI content, keep it brief.",
        height=100
    )

    max_iterations = st.slider("Max iterations", 5, 15, 8)

    if st.button("🚀 Run Agent", type="primary", disabled=not api_key):
        if not api_key:
            st.error("Enter API key in sidebar")
        else:
            agent = MultiProviderAgenticAgent(provider, api_key)

            try:
                agent.run_with_visualization(user_goal, max_iterations)
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
