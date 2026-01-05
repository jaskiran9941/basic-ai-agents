#!/bin/bash

# Browser MCP Agent - Streamlit Launcher

echo "🚀 Starting Browser MCP Agent with Streamlit UI..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Load .env file if it exists
if [ -f ".env" ]; then
    echo "📁 Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set. You'll need to enter it in the UI."
    echo ""
else
    echo "✅ OpenAI API key loaded from environment"
    echo ""
fi

# Run Streamlit
echo "🌐 Launching Streamlit at http://localhost:8501"
echo ""
echo "📖 Instructions:"
echo "   1. Enter your Anthropic API key in the sidebar"
echo "   2. Type browser commands in the chat input"
echo "   3. Watch the browser window as it executes commands"
echo "   4. Screenshots will appear in the right panel"
echo ""

streamlit run streamlit_app.py
