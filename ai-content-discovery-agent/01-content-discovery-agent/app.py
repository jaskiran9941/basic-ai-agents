"""
Streamlit Web App for Content Discovery Agent - Improved UX

Clean, modern interface with integrated clickable links for all sources.
"""

import streamlit as st
from agent import ContentDiscoveryAgent
import time

# Page configuration
st.set_page_config(
    page_title="Content Discovery Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .source-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #4CAF50;
    }
    .result-item {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        background-color: white;
        border: 1px solid #e0e0e0;
    }
    .result-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a73e8;
        margin-bottom: 0.5rem;
    }
    .result-meta {
        color: #666;
        font-size: 0.9rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Examples")

    examples = {
        "💻 Technical": [
            "React hooks tutorial",
            "Python machine learning",
            "Docker best practices"
        ],
        "📚 Learning": [
            "AI Product Management",
            "Data science career",
            "Quantum computing basics"
        ],
        "🏠 Lifestyle": [
            "Being a better partner",
            "Meditation for beginners",
            "Parenting toddlers"
        ]
    }

    for category, topics in examples.items():
        st.markdown(f"**{category}**")
        for topic in topics:
            if st.button(topic, key=topic, use_container_width=True):
                st.session_state.selected_topic = topic
        st.markdown("")

    st.divider()
    st.markdown("### ℹ️ About")
    st.caption("""
    This agent uses 6 data sources:
    - 🌐 Web Search
    - 💻 GitHub
    - 📚 Books
    - 🎥 YouTube
    - 💬 Reddit
    - 📄 arXiv Papers

    The agent decides which sources to use based on your topic.
    """)

# Main content
st.markdown('<h1 class="main-header">🤖 Content Discovery Agent</h1>', unsafe_allow_html=True)
st.markdown("**Intelligent resource discovery powered by AI** • Searches 6+ sources • Quality filtered")

st.divider()

# Input section
col1, col2 = st.columns([4, 1])

with col1:
    topic = st.text_input(
        "What do you want to learn about?",
        value=st.session_state.get('selected_topic', ''),
        placeholder="e.g., AI Product Management, React hooks, meditation...",
        label_visibility="collapsed",
        key="topic_input"
    )

with col2:
    search_button = st.button("🔍 Discover", type="primary", use_container_width=True)

# Results section
if search_button or st.session_state.get('selected_topic'):
    if 'selected_topic' in st.session_state:
        topic = st.session_state.selected_topic
        del st.session_state.selected_topic

    if not topic:
        st.warning("⚠️ Please enter a topic first!")
    else:
        # Initialize agent
        agent = ContentDiscoveryAgent()

        with st.spinner(f"🤖 Analyzing '{topic}' and searching sources..."):
            start_time = time.time()
            result = agent.discover(topic, verbose=False)
            elapsed_time = time.time() - start_time

        st.success(f"✅ Completed in {elapsed_time:.1f}s")

        # Metrics row
        st.divider()
        cols = st.columns(4)

        with cols[0]:
            st.metric("Sources Used", len(result['tools_used']))
        with cols[1]:
            st.metric("Total Results", sum(t['total'] for t in result['tools_used']))
        with cols[2]:
            st.metric("Cost", f"${result['estimated_cost']:.4f}")
        with cols[3]:
            st.metric("Tools Skipped", 6 - len(result['tools_used']))

        # Agent's summary
        st.divider()
        st.markdown("### 🎯 Agent's Curated Recommendations")

        if 'error' in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            with st.container():
                st.markdown(result['results'])

        # Sources section - REDESIGNED
        st.divider()
        st.markdown("### 📚 All Sources Discovered")
        st.caption("Click any title to visit the source")

        # Organize tools by category
        tool_icons = {
            'web_search': '🌐',
            'github_search': '💻',
            'books_search': '📚',
            'youtube_search': '🎥',
            'reddit_search': '💬',
            'arxiv_search': '📄'
        }

        tool_names = {
            'web_search': 'Web Articles',
            'github_search': 'GitHub Repositories',
            'books_search': 'Books',
            'youtube_search': 'YouTube Videos',
            'reddit_search': 'Reddit Discussions',
            'arxiv_search': 'Research Papers'
        }

        for tool_result in result['tools_used']:
            tool_name = tool_result['tool']
            icon = tool_icons.get(tool_name, '📁')
            display_name = tool_names.get(tool_name, tool_name.replace('_', ' ').title())

            with st.expander(f"{icon} **{display_name}** ({tool_result['total']} results)", expanded=False):
                if tool_result['success'] and tool_result['raw_results']:
                    st.caption(f"Search query: *{tool_result['query']}*")
                    st.markdown("")

                    for i, item in enumerate(tool_result['raw_results'], 1):
                        # Get title and URL
                        title = item.get('title', item.get('name', 'Untitled'))
                        url = item.get('url', item.get('info_link', ''))

                        # Create clickable title
                        if url:
                            st.markdown(f"**{i}. [{title}]({url})**")
                        else:
                            st.markdown(f"**{i}. {title}**")

                        # Show relevant metadata based on source type
                        meta_parts = []

                        # For web/articles
                        if 'content' in item:
                            content = item['content'][:150]
                            st.caption(content + "..." if len(item.get('content', '')) > 150 else content)

                        # For books
                        elif 'authors' in item:
                            meta_parts.append(f"✍️ {item['authors']}")
                            if item.get('rating') != 'N/A':
                                meta_parts.append(f"⭐ {item['rating']}/5")
                            if item.get('published_date'):
                                meta_parts.append(f"📅 {item['published_date']}")

                            if meta_parts:
                                st.caption(" • ".join(meta_parts))

                            if 'description' in item:
                                desc = item['description'][:150]
                                st.caption(desc + "..." if len(item.get('description', '')) > 150 else desc)

                        # For GitHub
                        elif 'stars' in item:
                            if item.get('language'):
                                meta_parts.append(f"💻 {item['language']}")
                            meta_parts.append(f"⭐ {item['stars']:,} stars")

                            if meta_parts:
                                st.caption(" • ".join(meta_parts))

                            if 'description' in item:
                                st.caption(item['description'])

                        # For YouTube
                        elif 'channel' in item:
                            meta_parts.append(f"📺 {item['channel']}")
                            if item.get('published_at'):
                                meta_parts.append(f"📅 {item['published_at']}")

                            if meta_parts:
                                st.caption(" • ".join(meta_parts))

                            if 'description' in item:
                                desc = item['description'][:150]
                                st.caption(desc + "..." if len(item.get('description', '')) > 150 else desc)

                        # For Reddit
                        elif 'subreddit' in item:
                            meta_parts.append(f"💬 {item['subreddit']}")
                            meta_parts.append(f"⬆️ {item.get('score', 0)} upvotes")
                            meta_parts.append(f"💭 {item.get('num_comments', 0)} comments")

                            if meta_parts:
                                st.caption(" • ".join(meta_parts))

                            if 'content' in item and item['content']:
                                content = item['content'][:150]
                                st.caption(content + "..." if len(item.get('content', '')) > 150 else content)

                        # For arXiv
                        elif 'authors' in item and 'arxiv' in url:
                            meta_parts.append(f"✍️ {item['authors']}")
                            if item.get('category'):
                                meta_parts.append(f"📂 {item['category']}")
                            if item.get('published_date'):
                                meta_parts.append(f"📅 {item['published_date']}")

                            if meta_parts:
                                st.caption(" • ".join(meta_parts))

                            if 'summary' in item:
                                summary = item['summary'][:200]
                                st.caption(summary + "..." if len(item.get('summary', '')) > 200 else summary)

                        st.markdown("")  # Spacing

                else:
                    st.warning(f"⚠️ No results or error occurred")

        # Skipped tools
        all_tools = ['web_search', 'github_search', 'books_search', 'youtube_search', 'reddit_search', 'arxiv_search']
        used_tools = [t['tool'] for t in result['tools_used']]
        skipped_tools = [t for t in all_tools if t not in used_tools]

        if skipped_tools:
            st.divider()
            st.markdown("### ⏭️ Skipped Sources")
            skipped_names = [f"{tool_icons.get(t, '•')} {tool_names.get(t, t)}" for t in skipped_tools]
            st.caption(f"The agent decided these weren't relevant: {', '.join(skipped_names)}")
            st.caption("💡 This shows intelligent tool selection - only using relevant sources!")

# Footer
st.divider()
st.caption("🤖 Built with Claude • All sources are live and clickable")
