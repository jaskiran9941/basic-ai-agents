"""
YouTube search tool using YouTube Data API v3.

Searches for relevant videos, tutorials, and educational content.
Great for visual learners and finding practical demonstrations.

Learning points:
- API key authentication
- Quota management (YouTube has daily limits)
- Pagination and result filtering
- Video metadata extraction
"""

import requests
from typing import Dict, List, Any
from config import Config


def youtube_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search YouTube for relevant videos.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dict containing:
        - success: bool
        - results: List of video results
        - error: str (if success is False)

    Example:
        >>> result = youtube_search("React hooks tutorial")
        >>> print(result['results'][0]['title'])
    """
    try:
        # YouTube Data API endpoint
        url = "https://www.googleapis.com/youtube/v3/search"

        # Query parameters
        params = {
            "part": "snippet",
            "q": query,
            "key": Config.GOOGLE_BOOKS_API_KEY,  # Same key works for YouTube
            "maxResults": max_results,
            "type": "video",
            "order": "relevance",
            "safeSearch": "moderate"
        }

        # Make API request
        response = requests.get(
            url,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Parse response
        data = response.json()

        # Format results
        results = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]

            # Get video statistics (views, likes) - requires separate API call
            # For simplicity, we'll skip this and just get basic info

            results.append({
                "title": snippet.get("title", ""),
                "description": snippet.get("description", "")[:300],  # Truncate
                "channel": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", "")[:10],  # Just date
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", "")
            })

        return {
            "success": True,
            "results": results,
            "total": len(results)
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. YouTube API took too long to respond.",
            "results": []
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 400:
            error_msg = "Bad request. Check your search query."
        elif status_code == 403:
            error_msg = "API quota exceeded or key invalid. YouTube has daily limits."
        else:
            error_msg = f"HTTP error occurred: {status_code}"

        return {
            "success": False,
            "error": error_msg,
            "results": []
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "results": []
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "results": []
        }


# Tool definition for Claude
YOUTUBE_SEARCH_TOOL = {
    "name": "youtube_search",
    "description": (
        "Search YouTube for relevant videos, tutorials, and educational content. "
        "Best for topics where visual demonstrations, walkthroughs, or video tutorials "
        "would be helpful. Returns video title, description, channel, and URL. "
        "Use this when users want to learn through videos or see practical demonstrations. "
        "Great for technical tutorials, how-to guides, and educational content."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for YouTube videos. Include relevant keywords and context."
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (1-10). Default is 5.",
                "default": 5
            }
        },
        "required": ["query"]
    }
}
