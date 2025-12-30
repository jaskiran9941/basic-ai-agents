"""
GitHub repository search tool.

Uses GitHub REST API to search for relevant repositories.
This tool is useful for technical topics where code examples or projects exist.

Learning points:
- Token-based authentication (Bearer token)
- Query parameter construction
- Pagination handling
- Rate limiting (5000 requests/hour for authenticated)
- Custom headers for API versioning
"""

import requests
from typing import Dict, List, Any
from config import Config


def github_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search GitHub repositories.

    Args:
        query: Search query (can include qualifiers like 'language:python')
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dict containing:
        - success: bool
        - results: List of repository results
        - error: str (if success is False)

    Example:
        >>> result = github_search("AI product management")
        >>> print(result['results'][0]['name'])
    """
    try:
        # GitHub API endpoint for repository search
        url = "https://api.github.com/search/repositories"

        # Headers for authentication and API version
        headers = {
            "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        # Query parameters
        params = {
            "q": query,
            "sort": "stars",  # Sort by popularity
            "order": "desc",
            "per_page": max_results
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
        for repo in data.get("items", []):
            results.append({
                "name": repo.get("full_name", ""),
                "description": repo.get("description", "No description provided"),
                "url": repo.get("html_url", ""),
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language", "Not specified"),
                "topics": repo.get("topics", []),
                "last_updated": repo.get("updated_at", "")
            })

        return {
            "success": True,
            "results": results,
            "total": len(results)
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. GitHub API took too long to respond.",
            "results": []
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 401:
            error_msg = "Authentication failed. Check your GitHub token."
        elif status_code == 403:
            error_msg = "Rate limit exceeded or token doesn't have required permissions."
        elif status_code == 422:
            error_msg = "Invalid search query. Check your search syntax."
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
GITHUB_SEARCH_TOOL = {
    "name": "github_search",
    "description": (
        "Search GitHub for relevant code repositories and projects. "
        "Best for technical topics where open-source projects, code examples, "
        "or developer tools are relevant. Returns repository name, description, "
        "stars, programming language, and URL. "
        "Use this for software development, programming, technical tools, or when "
        "the user wants to find code implementations or projects."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Search query for GitHub repositories. Can include qualifiers like "
                    "'language:python' or 'stars:>1000'. Be specific about what you're looking for."
                )
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
