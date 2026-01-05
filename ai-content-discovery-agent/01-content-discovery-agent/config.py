"""
Configuration management for the Content Discovery Agent.

This module loads API keys from environment variables and provides
configuration settings for the agent.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for managing API keys and settings."""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")  # For Phase 2

    # Agent settings
    CLAUDE_MODEL = "claude-3-haiku-20240307"  # Fast and capable for tool use
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7  # Balance between creativity and consistency

    # API settings
    MAX_SEARCH_RESULTS = 5  # Per tool
    REQUEST_TIMEOUT = 30  # seconds

    @classmethod
    def validate(cls):
        """Validate that required API keys are present."""
        required = {
            "ANTHROPIC_API_KEY": cls.ANTHROPIC_API_KEY,
            "TAVILY_API_KEY": cls.TAVILY_API_KEY,
            "GITHUB_TOKEN": cls.GITHUB_TOKEN,
            "GOOGLE_BOOKS_API_KEY": cls.GOOGLE_BOOKS_API_KEY,
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing)}\n"
                f"Please set them in your .env file.\n"
                f"See .env.example for reference."
            )

        return True


# Validate configuration on import
if __name__ != "__main__":
    try:
        Config.validate()
    except ValueError as e:
        print(f"⚠️  Configuration Error: {e}")
