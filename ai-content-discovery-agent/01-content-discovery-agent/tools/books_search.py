"""
Google Books search tool.

Uses Google Books API to search for relevant books.
Great for topics where deep reading or comprehensive guides are valuable.

Learning points:
- API key authentication via query parameter
- Handling optional parameters
- Parsing nested JSON responses
- Dealing with incomplete data (not all books have all fields)
"""

import requests
from typing import Dict, List, Any
from config import Config


def is_book_relevant(book: Dict[str, Any], query: str) -> bool:
    """
    Check if a book is relevant to the query.

    Filters out:
    - Books with no description
    - Books with very short descriptions (< 50 chars)
    - Books with generic/placeholder titles
    - Books that seem completely off-topic
    """
    title = book.get('title', '').lower()
    description = book.get('description', '')

    # Filter out books with no description
    if description == "No description available" or len(description) < 50:
        return False

    # Filter out obviously generic titles
    generic_titles = ['the architect', 'the builder', 'the engineer', 'the republic']
    if any(generic in title for generic in generic_titles):
        return False

    # Check if query terms appear in title or description
    query_terms = query.lower().split()
    text_to_check = (title + ' ' + description.lower())

    # At least 2 query terms should appear (or 1 if query is short)
    min_matches = 1 if len(query_terms) <= 2 else 2
    matches = sum(1 for term in query_terms if term in text_to_check)

    return matches >= min_matches


def books_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search Google Books for relevant books.

    Args:
        query: Search query
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dict containing:
        - success: bool
        - results: List of book results
        - error: str (if success is False)

    Example:
        >>> result = books_search("AI Product Management")
        >>> print(result['results'][0]['title'])
    """
    try:
        # Google Books API endpoint
        url = "https://www.googleapis.com/books/v1/volumes"

        # Query parameters
        params = {
            "q": query,
            "key": Config.GOOGLE_BOOKS_API_KEY,
            "maxResults": min(max_results, 40),  # API max is 40
            "orderBy": "relevance",
            "printType": "books"
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

        # Format results with quality filtering
        results = []
        raw_results = []

        # Get more results than needed for filtering
        for item in data.get("items", [])[:max_results * 3]:
            volume_info = item.get("volumeInfo", {})

            # Extract authors (can be a list)
            authors = volume_info.get("authors", ["Unknown Author"])
            authors_str = ", ".join(authors)

            # Get published date
            published_date = volume_info.get("publishedDate", "Unknown")

            # Get rating info
            rating = volume_info.get("averageRating", "N/A")
            rating_count = volume_info.get("ratingsCount", 0)

            # Get description (truncate if too long)
            description = volume_info.get("description", "No description available")
            if len(description) > 300:
                description = description[:297] + "..."

            # Get book links
            info_link = volume_info.get("infoLink", "")
            preview_link = volume_info.get("previewLink", "")

            book_data = {
                "title": volume_info.get("title", "Unknown Title"),
                "authors": authors_str,
                "published_date": published_date,
                "description": description,
                "rating": rating,
                "rating_count": rating_count,
                "page_count": volume_info.get("pageCount", "Unknown"),
                "categories": volume_info.get("categories", []),
                "info_link": info_link,
                "preview_link": preview_link
            }
            raw_results.append(book_data)

        # Filter results for relevance
        filtered_results = [book for book in raw_results if is_book_relevant(book, query)]

        # Take only the requested number after filtering
        results = filtered_results[:max_results]

        return {
            "success": True,
            "results": results,
            "total": len(results),
            "filtered_count": len(raw_results) - len(filtered_results)  # How many we filtered out
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Google Books API took too long to respond.",
            "results": []
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 400:
            error_msg = "Bad request. Check your search query."
        elif status_code == 401:
            error_msg = "Authentication failed. Check your Google Books API key."
        elif status_code == 403:
            error_msg = "API key invalid or quota exceeded."
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
BOOKS_SEARCH_TOOL = {
    "name": "books_search",
    "description": (
        "Search Google Books for relevant books and publications. "
        "Best for topics where comprehensive guides, deep reading, or structured "
        "learning materials are valuable. Returns book title, authors, description, "
        "ratings, and links. "
        "Use this when the user wants authoritative sources, in-depth learning "
        "resources, or classic references on a topic."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for books. Include topic keywords and optionally author names."
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
