"""
Reddit search tool using Reddit API.

Searches for discussions, user experiences, and community insights.
Great for real-world perspectives and practical advice.

Learning points:
- User-Agent header requirement (Reddit requires this)
- Rate limiting without authentication
- Sorting and filtering options
- Community-driven content
"""

import requests
from typing import Dict, List, Any
from config import Config


def reddit_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search Reddit for relevant discussions and posts.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dict containing:
        - success: bool
        - results: List of Reddit post results
        - error: str (if success is False)

    Example:
        >>> result = reddit_search("AI product management")
        >>> print(result['results'][0]['title'])
    """
    try:
        # Reddit API endpoint (no auth required for search)
        url = "https://www.reddit.com/search.json"

        # Headers (Reddit requires User-Agent)
        headers = {
            "User-Agent": "ContentDiscoveryAgent/1.0 (Educational Project)"
        }

        # Query parameters
        params = {
            "q": query,
            "limit": max_results,
            "sort": "relevance",
            "type": "link"  # Only posts, not comments
        }

        # Make API request
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Parse response
        data = response.json()

        # Format results
        results = []
        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})

            results.append({
                "title": post_data.get("title", ""),
                "subreddit": post_data.get("subreddit_name_prefixed", ""),
                "author": post_data.get("author", ""),
                "score": post_data.get("score", 0),
                "num_comments": post_data.get("num_comments", 0),
                "url": f"https://www.reddit.com{post_data.get('permalink', '')}",
                "content": post_data.get("selftext", "")[:300],  # Truncate
                "created": post_data.get("created_utc", 0)
            })

        return {
            "success": True,
            "results": results,
            "total": len(results)
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Reddit API took too long to respond.",
            "results": []
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 429:
            error_msg = "Rate limit exceeded. Reddit limits unauthenticated requests."
        elif status_code == 403:
            error_msg = "Access forbidden. Check User-Agent header."
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
REDDIT_SEARCH_TOOL = {
    "name": "reddit_search",
    "description": (
        "Search Reddit for community discussions, user experiences, and practical advice. "
        "Best for finding real-world perspectives, troubleshooting tips, and community insights. "
        "Returns post title, subreddit, discussion URL, score, and number of comments. "
        "Use this when users want to see what real people are saying, common problems, "
        "or community recommendations. Great for getting unfiltered opinions and experiences."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for Reddit discussions. Use natural language."
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
