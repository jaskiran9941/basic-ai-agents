"""
arXiv search tool for academic papers.

Searches the arXiv repository for scientific and academic papers.
Great for research, technical deep-dives, and cutting-edge developments.

Learning points:
- XML API response parsing
- Academic paper metadata
- No authentication required (fully open)
- Field-specific searches
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from config import Config


def arxiv_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search arXiv for academic papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dict containing:
        - success: bool
        - results: List of paper results
        - error: str (if success is False)

    Example:
        >>> result = arxiv_search("machine learning")
        >>> print(result['results'][0]['title'])
    """
    try:
        # arXiv API endpoint
        url = "http://export.arxiv.org/api/query"

        # Query parameters
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        # Make API request
        response = requests.get(
            url,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.content)

        # Namespace for arXiv API
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

        # Format results
        results = []
        for entry in root.findall('atom:entry', ns):
            # Extract authors
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns)
                if name is not None:
                    authors.append(name.text)

            # Get primary category
            primary_category = entry.find('arxiv:primary_category', ns)
            category = primary_category.get('term') if primary_category is not None else 'Unknown'

            # Get published date
            published = entry.find('atom:published', ns)
            published_date = published.text[:10] if published is not None else 'Unknown'

            # Get title and summary
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.replace('\n', ' ').strip() if title_elem is not None else 'No title'

            summary_elem = entry.find('atom:summary', ns)
            summary = summary_elem.text.replace('\n', ' ').strip()[:300] if summary_elem is not None else ''

            # Get URL
            link = entry.find('atom:id', ns)
            paper_url = link.text if link is not None else ''

            results.append({
                "title": title,
                "authors": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
                "summary": summary,
                "category": category,
                "published_date": published_date,
                "url": paper_url,
                "pdf_url": paper_url.replace('/abs/', '/pdf/') + '.pdf' if paper_url else ''
            })

        return {
            "success": True,
            "results": results,
            "total": len(results)
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. arXiv API took too long to respond.",
            "results": []
        }

    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP error occurred: {e.response.status_code}",
            "results": []
        }

    except ET.ParseError as e:
        return {
            "success": False,
            "error": f"Failed to parse XML response: {str(e)}",
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
ARXIV_SEARCH_TOOL = {
    "name": "arxiv_search",
    "description": (
        "Search arXiv for academic papers and research publications. "
        "Best for scientific and technical topics where cutting-edge research, "
        "theoretical foundations, or academic perspectives are valuable. "
        "Returns paper title, authors, abstract, category, and PDF link. "
        "Use this for AI/ML topics, computer science, physics, mathematics, "
        "and other scientific fields. Great for understanding state-of-the-art research."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for academic papers. Use technical terms and keywords."
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
