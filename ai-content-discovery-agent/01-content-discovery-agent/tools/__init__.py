"""
Tools package for the Content Discovery Agent.

This package contains implementations for various search tools:
- web_search: Uses Tavily API for web search
- github_search: Uses GitHub API for repository search
- books_search: Uses Google Books API for book search
- youtube_search: Uses YouTube Data API for video search
- reddit_search: Uses Reddit API for community discussions
- arxiv_search: Uses arXiv API for academic papers
"""

from .web_search import web_search
from .github_search import github_search
from .books_search import books_search
from .youtube_search import youtube_search
from .reddit_search import reddit_search
from .arxiv_search import arxiv_search

__all__ = [
    "web_search",
    "github_search",
    "books_search",
    "youtube_search",
    "reddit_search",
    "arxiv_search"
]
