#!/bin/bash

echo "🚀 Starting Startup Guillotine Setup..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Node.js and Python are installed"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get your API keys:"
echo "   - Google AI Studio: https://makersuite.google.com/app/apikey"
echo "   - Tavily: https://tavily.com"
echo ""
echo "2. For LOCAL development, create .env files:"
echo "   - Create .env in root directory with:"
echo "     GOOGLE_AI_API_KEY=your_gemini_api_key_here"
echo "     TAVILY_API_KEY=your_tavily_api_key_here"
echo "     CORS_ORIGINS=http://localhost:3000"
echo "     NEXT_PUBLIC_BACKEND_URL=http://localhost:8000"
echo ""
echo "3. For VERCEL deployment, set environment variables in Vercel dashboard:"
echo "   - GOOGLE_AI_API_KEY"
echo "   - TAVILY_API_KEY"
echo "   - CORS_ORIGINS"
echo "   - NEXT_PUBLIC_BACKEND_URL"
echo ""
echo "4. Start development servers:"
echo "   npm run dev"
echo ""
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For deployment instructions, see DEPLOYMENT.md" 