"""
Web search tool using Tavily API.

Tavily is optimized for LLM agents and provides clean, structured results.
This is our primary tool for finding blogs, articles, and general web content.

Learning points:
- Simple REST API with API key authentication
- JSON request/response
- Error handling and timeouts
- Rate limiting considerations
"""

import requests
from typing import Dict, List, Any
from config import Config


def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search the web using Tavily API.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dict containing:
        - success: bool
        - results: List of search results
        - error: str (if success is False)

    Example:
        >>> result = web_search("AI Product Management blogs")
        >>> print(result['results'][0]['title'])
    """
    try:
        # Tavily API endpoint
        url = "https://api.tavily.com/search"

        # Request payload
        payload = {
            "api_key": Config.TAVILY_API_KEY,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",  # "basic" or "advanced"
            "include_answer": False,  # We'll let Claude synthesize
            "include_raw_content": False,  # Keep response size small
        }

        # Make API request
        response = requests.post(
            url,
            json=payload,
            timeout=Config.REQUEST_TIMEOUT
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Parse response
        data = response.json()

        # Format results
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "score": item.get("score", 0),
            })

        return {
            "success": True,
            "results": results,
            "total": len(results)
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. The API took too long to respond.",
            "results": []
        }

    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP error occurred: {e.response.status_code}",
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
WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": (
        "Search the web for current information, articles, and blogs. "
        "Best for finding recent content, articles, blog posts, and general information. "
        "Use this when the user wants to find online resources, current trends, or "
        "up-to-date information on any topic."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query. Be specific and include relevant keywords."
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
