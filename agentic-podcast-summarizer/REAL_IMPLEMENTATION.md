# How to Make This TRULY Search Podcasts

## Current State: Mock Data

The current `execute_tool()` method returns **hardcoded data**:

```python
def execute_tool(self, tool_name: str, tool_args: Dict) -> Dict:
    if tool_name == "fetch_new_episodes":
        # ❌ FAKE: Returns hardcoded episodes
        episodes = [
            {"title": "Yann LeCun: AI Safety...", ...},
            {"title": "Gordon Ramsay Cooking...", ...}
        ]
        return {"episodes": episodes}
```

## What You'd Need to Change

### Option 1: Connect to Non-Agentic Project

```python
# Add to app.py imports:
import sys
sys.path.insert(0, "../../llm-apps/podcast-summarizer/src")
from podcast_fetcher import PodcastFetcher
from transcript_fetcher import TranscriptFetcher
from summarizer import PodcastSummarizer

class OpenAIAgenticAgent:
    def __init__(self, api_key: str):
        # ... existing code ...

        # ✅ ADD: Real podcast modules
        self.podcast_fetcher = PodcastFetcher()
        self.transcript_fetcher = TranscriptFetcher()
        self.real_summarizer = PodcastSummarizer()

    def execute_tool(self, tool_name: str, tool_args: Dict) -> Dict:
        if tool_name == "fetch_new_episodes":
            # ✅ REAL: Call actual RSS fetcher
            hours_back = tool_args.get("hours_back", 24)
            episodes = self.podcast_fetcher.fetch_new_episodes(
                since_hours=hours_back
            )
            return {"success": True, "episodes": episodes}

        elif tool_name == "get_transcript":
            # ✅ REAL: Fetch actual transcript
            episode = tool_args.get("episode")
            transcript = self.transcript_fetcher.get_transcript(episode)
            return {"transcript": transcript}

        elif tool_name == "generate_summary":
            # ✅ REAL: Use OpenAI to summarize
            episode = tool_args.get("episode")
            transcript = tool_args.get("transcript")
            summary = self.real_summarizer.summarize_episode(episode, transcript)
            return {"summary": summary}
```

### Option 2: Use Podcast APIs

If you want to search **new** podcasts (like Apple Podcasts or Spotify):

```python
import requests

def execute_tool(self, tool_name: str, tool_args: Dict) -> Dict:
    if tool_name == "search_web_for_podcasts":
        topics = tool_args.get("topics", [])

        # ✅ REAL: Search iTunes/Apple Podcasts API
        search_term = " ".join(topics)
        response = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": search_term,
                "media": "podcast",
                "limit": 10
            }
        )

        results = response.json().get("results", [])
        podcasts = [
            {
                "name": r["collectionName"],
                "rss_url": r["feedUrl"],
                "description": r.get("description", ""),
                "artwork": r.get("artworkUrl600", "")
            }
            for r in results
        ]

        return {"success": True, "recommendations": podcasts}
```

**Available Podcast APIs:**
- **iTunes Search API** (free, no key needed)
  - `https://itunes.apple.com/search`
  - Searches Apple Podcasts catalog

- **Listen Notes API** (paid, comprehensive)
  - `https://www.listennotes.com/api/`
  - Search podcasts, episodes, get transcripts

- **Podcast Index API** (free with API key)
  - `https://podcastindex.org/`
  - Open podcast directory

- **Spotify API** (free with OAuth)
  - Requires authentication
  - Access Spotify podcast catalog

### Option 3: Full Real Implementation

```python
import feedparser
import requests
from openai import OpenAI

class RealAgenticPodcastAgent:
    def __init__(self, api_key: str):
        self.openai_client = OpenAI(api_key=api_key)
        self.podcast_subscriptions = [
            "https://lexfridman.com/feed/podcast/",
            "https://rss.art19.com/tim-ferriss-show"
        ]

    def execute_tool(self, tool_name: str, tool_args: Dict) -> Dict:
        if tool_name == "fetch_new_episodes":
            # ✅ REAL: Parse actual RSS feeds
            hours_back = tool_args.get("hours_back", 24)
            all_episodes = []

            for rss_url in self.podcast_subscriptions:
                feed = feedparser.parse(rss_url)
                for entry in feed.entries[:5]:  # Last 5 episodes
                    episode = {
                        "title": entry.title,
                        "description": entry.summary,
                        "audio_url": entry.enclosures[0].href if entry.enclosures else None,
                        "published": entry.published,
                        "podcast": feed.feed.title
                    }
                    all_episodes.append(episode)

            return {"success": True, "episodes": all_episodes}

        elif tool_name == "search_web_for_podcasts":
            # ✅ REAL: Search iTunes API
            topics = tool_args.get("topics", [])
            search_query = " ".join(topics)

            response = requests.get(
                "https://itunes.apple.com/search",
                params={"term": search_query, "media": "podcast", "limit": 5}
            )

            results = response.json().get("results", [])
            recommendations = [
                {
                    "name": r["collectionName"],
                    "rss_url": r.get("feedUrl", ""),
                    "description": r.get("description", "No description"),
                    "artist": r.get("artistName", "Unknown")
                }
                for r in results
            ]

            return {"success": True, "recommendations": recommendations}

        elif tool_name == "get_transcript":
            # ✅ REAL: Try to fetch transcript or use Whisper
            episode_url = tool_args.get("audio_url")

            # Try podcast platforms that provide transcripts
            # Or use OpenAI Whisper to transcribe audio

            # For now, simple description extraction:
            return {
                "transcript": tool_args.get("description", "No transcript available"),
                "source": "description"
            }

        elif tool_name == "generate_summary":
            # ✅ REAL: Use OpenAI to summarize
            transcript = tool_args.get("transcript")
            style = tool_args.get("style", "detailed")

            prompt = f"Summarize this podcast in {style} style:\n\n{transcript}"

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                "success": True,
                "summary": response.choices[0].message.content,
                "style_used": style
            }
```

## Architecture: Current vs Real

### Current (Mock):
```
User Goal → GPT-4 decides tools → execute_tool() returns hardcoded data
```

### Real Implementation:
```
User Goal
    ↓
GPT-4 decides: "search_web_for_podcasts"
    ↓
execute_tool() → iTunes API → Real podcast results
    ↓
GPT-4 decides: "fetch_new_episodes"
    ↓
execute_tool() → feedparser → Parse real RSS feeds
    ↓
GPT-4 decides: "get_transcript"
    ↓
execute_tool() → Podcast website or Whisper API → Real transcript
    ↓
GPT-4 decides: "generate_summary"
    ↓
execute_tool() → OpenAI GPT-4 → Real summary
    ↓
GPT-4 decides: "send_email"
    ↓
execute_tool() → SendGrid API → Real email
```

## Why Use Mock Data?

**Educational Purpose:**
- ✅ Demonstrates agentic decision-making patterns
- ✅ Shows how AI chooses tools dynamically
- ✅ Fast execution (no waiting for API calls)
- ✅ No API costs during development/testing
- ✅ Predictable behavior for learning

**For Production:**
- Replace mock data with real API calls
- Add error handling for failed API requests
- Implement rate limiting
- Cache results
- Add retry logic

## Summary

**Current Project Focus:**
- 🎯 **Demonstrates:** How agents think and make decisions
- ❌ **Not:** A functional podcast search/summarization app

**To Make It Real:**
1. Import modules from `llm-apps/podcast-summarizer`
2. Or implement API calls to iTunes/Spotify/Listen Notes
3. Replace hardcoded data in `execute_tool()` with real API responses

**Key Insight:**
The agentic behavior (decision-making, tool selection, adaptation) is REAL.
The data it operates on is MOCK (for educational purposes).
