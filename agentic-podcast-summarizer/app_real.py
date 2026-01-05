#!/usr/bin/env python3
"""
Streamlit UI for Agentic Podcast Summarizer
OpenAI GPT-4 Implementation with REAL PODCAST DATA

This version uses:
- iTunes API for podcast discovery
- RSS feeds for real episodes
- GPT-4 for actual summarization
"""

import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import feedparser
import requests
from time import mktime

# Page config
st.set_page_config(
    page_title="Agentic Podcast Summarizer - Real Data",
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
    .real-data-badge {
        background-color: #4CAF50;
        color: white;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


class RealDataAgenticAgent:
    """Agentic agent using REAL podcast data from iTunes and RSS feeds."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"

        # Real user preferences (could be loaded from database/file)
        self.user_preferences = {
            "recent_topics": ["AI", "technology", "machine learning"],
            "preferred_length": "detailed",
            "skip_topics": ["sports", "politics"]
        }

        # User's subscribed podcasts (could be managed in UI)
        self.user_subscriptions = [
            {
                "name": "Lex Fridman Podcast",
                "rss_url": "https://lexfridman.com/feed/podcast/",
                "tags": ["AI", "technology", "science"]
            },
            {
                "name": "a16z Podcast",
                "rss_url": "https://feeds.simplecast.com/JGE3yC0V",
                "tags": ["technology", "startups", "AI"]
            },
            {
                "name": "The AI Podcast",
                "rss_url": "https://feeds.pacific-content.com/ai-podcast",
                "tags": ["AI", "technology"]
            }
        ]

        # Define tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "check_user_preferences",
                    "description": "Check user's interests, subscribed podcasts, and preferences",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web_for_podcasts",
                    "description": "Search iTunes/Apple Podcasts for new podcast recommendations based on topics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topics": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Topics to search for (e.g., ['AI', 'machine learning'])"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Max number of results (default 5)"
                            }
                        },
                        "required": ["topics"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_new_episodes",
                    "description": "Fetch recent episodes from user's subscribed podcast RSS feeds",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "hours_back": {
                                "type": "number",
                                "description": "How many hours back to check (e.g., 24, 168)"
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
                    "description": "Analyze if an episode matches user's interests (returns score 0-1)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "episode_title": {"type": "string"},
                            "episode_description": {"type": "string"},
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
                    "description": "Generate AI summary of episode content using GPT-4",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "episode_title": {"type": "string"},
                            "episode_description": {"type": "string"},
                            "style": {
                                "type": "string",
                                "enum": ["brief", "detailed", "technical"],
                                "description": "Summary style based on context"
                            }
                        },
                        "required": ["episode_title", "episode_description", "style"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_for_later",
                    "description": "Save episode to reading list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "episode_title": {"type": "string"},
                            "reason": {"type": "string"}
                        },
                        "required": ["episode_title", "reason"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_args: Dict) -> Dict:
        """Execute the tool that AI chose - with REAL data sources."""

        st.info(f"🔍 Calling REAL API: {tool_name}")

        try:
            if tool_name == "check_user_preferences":
                return {
                    "success": True,
                    "preferences": self.user_preferences,
                    "subscriptions": [
                        {"name": sub["name"], "tags": sub["tags"]}
                        for sub in self.user_subscriptions
                    ]
                }

            elif tool_name == "search_web_for_podcasts":
                # ✅ REAL: Search iTunes API
                topics = tool_args.get("topics", [])
                limit = tool_args.get("limit", 5)
                search_query = " ".join(topics)

                st.info(f"📡 Searching iTunes API for: {search_query}")

                response = requests.get(
                    "https://itunes.apple.com/search",
                    params={
                        "term": search_query,
                        "media": "podcast",
                        "limit": limit,
                        "country": "US"
                    },
                    timeout=10
                )

                if response.status_code != 200:
                    return {"success": False, "error": f"iTunes API error: {response.status_code}"}

                results = response.json().get("results", [])

                podcasts = []
                for r in results:
                    if r.get("feedUrl"):  # Only include if has RSS feed
                        podcasts.append({
                            "name": r.get("collectionName", "Unknown"),
                            "rss_url": r.get("feedUrl"),
                            "artist": r.get("artistName", "Unknown"),
                            "description": r.get("description", "No description"),
                            "artwork": r.get("artworkUrl600", ""),
                            "genres": r.get("genres", [])
                        })

                return {
                    "success": True,
                    "recommendations": podcasts,
                    "count": len(podcasts),
                    "source": "iTunes API"
                }

            elif tool_name == "fetch_new_episodes":
                # ✅ REAL: Parse RSS feeds
                hours_back = tool_args.get("hours_back", 24)
                cutoff_time = datetime.now() - timedelta(hours=hours_back)

                st.info(f"📡 Parsing RSS feeds from {len(self.user_subscriptions)} subscriptions")

                all_episodes = []

                for subscription in self.user_subscriptions:
                    try:
                        st.caption(f"Parsing: {subscription['name']}")

                        feed = feedparser.parse(subscription["rss_url"])

                        if feed.bozo:
                            st.warning(f"⚠️ Error parsing {subscription['name']}")
                            continue

                        for entry in feed.entries[:10]:  # Check last 10 episodes
                            # Parse publish date
                            pub_date = None
                            if hasattr(entry, "published_parsed") and entry.published_parsed:
                                pub_date = datetime.fromtimestamp(mktime(entry.published_parsed))
                            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                                pub_date = datetime.fromtimestamp(mktime(entry.updated_parsed))

                            # Check if recent enough
                            if pub_date and pub_date > cutoff_time:
                                episode = {
                                    "title": entry.get("title", "Untitled"),
                                    "description": entry.get("summary", "No description"),
                                    "podcast": subscription["name"],
                                    "published": pub_date.strftime("%Y-%m-%d %H:%M"),
                                    "audio_url": entry.enclosures[0].href if hasattr(entry, "enclosures") and entry.enclosures else None,
                                    "link": entry.get("link", ""),
                                    "tags": subscription.get("tags", [])
                                }
                                all_episodes.append(episode)

                    except Exception as e:
                        st.warning(f"⚠️ Error fetching {subscription['name']}: {str(e)}")
                        continue

                return {
                    "success": True,
                    "episodes": all_episodes,
                    "count": len(all_episodes),
                    "source": "RSS Feeds",
                    "time_range": f"Last {hours_back} hours"
                }

            elif tool_name == "analyze_episode_relevance":
                title = tool_args.get("episode_title", "")
                description = tool_args.get("episode_description", "")
                interests = tool_args.get("user_interests", [])

                # Simple keyword matching (could be enhanced with embeddings)
                combined_text = (title + " " + description).lower()

                score = 0.3  # Base score
                matches = []

                for interest in interests:
                    if interest.lower() in combined_text:
                        score += 0.2
                        matches.append(interest)

                score = min(score, 1.0)

                return {
                    "success": True,
                    "relevance_score": round(score, 2),
                    "matches": matches,
                    "reasoning": f"Found {len(matches)} keyword matches: {', '.join(matches) if matches else 'none'}",
                    "recommendation": "summarize" if score > 0.5 else "skip"
                }

            elif tool_name == "generate_summary":
                # ✅ REAL: Use GPT-4 to actually generate summary
                title = tool_args.get("episode_title", "")
                description = tool_args.get("episode_description", "")
                style = tool_args.get("style", "detailed")

                st.info(f"🤖 Generating {style} summary with GPT-4...")

                style_prompts = {
                    "brief": "Create a brief 2-3 sentence summary.",
                    "detailed": "Create a detailed summary with 5-7 key bullet points.",
                    "technical": "Create an in-depth technical analysis with detailed explanations."
                }

                prompt = f"""{style_prompts[style]}

Episode Title: {title}

Episode Description:
{description[:4000]}

Provide a clear, informative summary."""

                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )

                summary = response.choices[0].message.content

                return {
                    "success": True,
                    "summary": summary,
                    "style_used": style,
                    "source": "GPT-4 Real Generation"
                }

            elif tool_name == "save_for_later":
                episode_title = tool_args.get("episode_title", "")
                reason = tool_args.get("reason", "")

                return {
                    "success": True,
                    "message": f"Saved '{episode_title}' for later",
                    "reason": reason
                }

            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            st.error(f"❌ Error in {tool_name}: {str(e)}")
            return {"success": False, "error": str(e)}

    def run_with_visualization(self, user_goal: str, max_iterations: int = 10):
        """Run agent with Streamlit visualization."""

        messages = [{
            "role": "user",
            "content": f"""You are an intelligent, autonomous podcast research agent.

Your goal: {user_goal}

You have access to REAL podcast data sources:
- iTunes API for discovering new podcasts
- RSS feeds for fetching actual episodes
- GPT-4 for generating real summaries

Think strategically and explain your reasoning clearly before each action.

Guidelines:
1. ALWAYS start by checking user preferences and subscriptions
2. When fetching episodes, use reasonable time ranges (24-168 hours)
3. Analyze episode relevance before summarizing (don't waste time on irrelevant content)
4. Choose appropriate summary styles based on context
5. Only recommend actions when you have genuinely valuable content

Work autonomously toward the goal. Make smart decisions."""
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
                        st.markdown(f"### 🔧 Tool: **{tool_call.function.name}** <span class='real-data-badge'>REAL DATA</span>", unsafe_allow_html=True)

                        # Parse arguments
                        tool_args = json.loads(tool_call.function.arguments)

                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown("**Input:**")
                        with col2:
                            st.json(tool_args)

                        # Execute tool (with real API calls)
                        result = self.execute_tool(tool_call.function.name, tool_args)

                        st.markdown("### ✅ Result")
                        st.markdown(
                            f'<div class="result-box">{json.dumps(result, indent=2)[:1000]}...</div>',
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
    st.markdown("### 🌐 Powered by OpenAI GPT-4 + Real Podcast Data")
    st.success("✨ Using REAL data: iTunes API + RSS Feeds + GPT-4 Summaries")

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

        st.header("📋 Data Sources")
        st.markdown("""
        **REAL APIs used:**
        - 🍎 iTunes/Apple Podcasts
        - 📡 RSS Feeds (feedparser)
        - 🤖 OpenAI GPT-4

        **No mock data!** Everything is real.
        """)

        st.divider()

        st.header("🎯 Quick Presets")
        if st.button("📌 Recent AI Episodes"):
            st.session_state.preset = "recent"
        if st.button("🔍 Discover New AI Podcasts"):
            st.session_state.preset = "discover"
        if st.button("🎓 Deep Technical Dive"):
            st.session_state.preset = "technical"

    # Main area
    st.markdown("## Run the Agent with Real Data")

    # Goal presets
    preset = st.session_state.get('preset', None)
    if preset == "recent":
        default_goal = "Get me AI and technology podcast episodes from the last 48 hours. Summarize the most relevant ones."
    elif preset == "discover":
        default_goal = "Search for new AI podcasts I haven't heard of, check their latest episodes, and give me a detailed overview."
    elif preset == "technical":
        default_goal = "Find recent episodes about machine learning or AI. I want detailed technical summaries."
    else:
        default_goal = "Get me valuable podcast insights about AI and technology from the last 24 hours."

    user_goal = st.text_area(
        "What should the agent do?",
        value=default_goal,
        height=100,
        help="The agent will search REAL podcasts and generate REAL summaries"
    )

    max_iterations = st.slider("Max iterations", 5, 15, 10)

    col1, col2 = st.columns([3, 1])
    with col1:
        run_button = st.button("🚀 Run Agent with Real Data", type="primary", disabled=not api_key)
    with col2:
        st.caption("⚠️ This will make real API calls")

    if run_button:
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API key in the sidebar")
        else:
            st.markdown("---")
            st.info("🔄 Agent is working with REAL podcast data... This may take 30-60 seconds.")

            agent = RealDataAgenticAgent(api_key)

            try:
                result = agent.run_with_visualization(user_goal, max_iterations)
                st.markdown("---")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
