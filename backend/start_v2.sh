#!/bin/bash

echo "🚀 Startup Guillotine Validation API v2.0 - Pure LLM Approach"
echo "================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env file with your API keys:"
    echo "   - GEMINI_API_KEY"
    echo "   - TAVILY_API_KEY"
    echo "   - REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT"
    echo ""
    echo "   See env.example for template"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# echo ""
# echo "🔍 Starting comprehensive test..."
# echo "================================================================"

# # Run comprehensive test
# python test_comprehensive_validation.py

# echo ""
# echo "================================================================"
# echo "🧪 Test completed! Starting API server..."
# echo ""

# Start the API server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔴 Press Ctrl+C to stop"
echo ""

uvicorn app:app --host 0.0.0.0 --port 8000 --reload 