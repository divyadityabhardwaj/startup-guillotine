# 🪓 Startup Guillotine

AI-powered startup idea validation using comprehensive market analysis, competitive intelligence, and business insights.

## 🚀 Features

- **Comprehensive Analysis**: Market assessment, competitive landscape, uniqueness analysis
- **Real-time Data**: Google Trends, competitor research, community sentiment
- **AI-Powered Insights**: Gemini 1.5 Flash for intelligent business analysis
- **File Support**: PDF upload and text input validation
- **Modern UI**: Beautiful, responsive frontend built with Next.js

## 🏗️ Architecture

- **Backend**: FastAPI with Python (Vercel serverless)
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **AI**: Google Gemini 1.5 Flash for analysis
- **Data Sources**: Tavily Search, Google Trends, Reddit API

## 🚀 Vercel Deployment

### Option 1: Single Vercel Project (Recommended)

Deploy both backend and frontend together as a monorepo:

1. **Fork/Clone Repository**:

   ```bash
   git clone <your-repo-url>
   cd startup-guillotine
   ```

2. **Install Dependencies**:

   ```bash
   npm run install:all
   ```

3. **Deploy to Vercel** (from root directory):

   ```bash
   vercel
   ```

4. **Set Environment Variables** in Vercel Dashboard:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_SECRET=your_reddit_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   ```

5. **Your app will be available at**: `https://your-project.vercel.app`

### Option 2: Separate Deployments

If you prefer separate deployments:

#### Backend Deployment

1. **Navigate to Backend**:

   ```bash
   cd backend
   ```

2. **Deploy to Vercel**:

   ```bash
   vercel
   ```

3. **Set Environment Variables** in Vercel Dashboard:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_SECRET=your_reddit_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   ```

4. **Note Backend URL**: Copy the deployment URL (e.g., `https://your-backend.vercel.app`)

#### Frontend Deployment

1. **Navigate to Frontend**:

   ```bash
   cd frontend
   ```

2. **Update Environment**:

   ```bash
   cp env.example .env.local
   ```

   Edit `.env.local`:

   ```env
   NEXT_PUBLIC_BACKEND_URL=https://your-backend.vercel.app
   ```

3. **Deploy to Vercel**:

   ```bash
   vercel
   ```

4. **Set Environment Variables** in Vercel Dashboard:
   ```env
   NEXT_PUBLIC_BACKEND_URL=https://your-backend.vercel.app
   ```

## 🧪 Local Development

### Development Setup

#### Backend

1. **Setup Environment**:

   ```bash
   cd backend
   cp env.example .env
   # Edit .env with your API keys
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Development Server**:

   ```bash
   python main.py
   ```

   Backend will be available at `http://localhost:8000`

#### Frontend

1. **Setup Environment**:

   ```bash
   cd frontend
   cp env.example .env.local
   # Edit .env.local with backend URL: http://localhost:8000
   ```

2. **Install Dependencies**:

   ```bash
   npm install
   ```

3. **Run Development Server**:

   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

### Running Both Services

You'll need two terminal windows:

**Terminal 1 (Backend)**:

```bash
cd backend
python main.py
```

**Terminal 2 (Frontend)**:

```bash
cd frontend
npm run dev
```

## 🔧 API Endpoints

### Backend (`/api/v1/`)

- `POST /validate` - Comprehensive startup idea validation
- `POST /validate-file` - File-based validation (PDF/DOCX)
- `POST /validate/quick` - Quick validation summary
- `GET /health` - Health check
- `GET /status` - Service status
- `GET /` - API information

### Frontend

- `/` - Main application
- File upload and text input support
- Real-time analysis display

## 📁 Project Structure

```
startup-guillotine/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── main.py             # Entry point
│   ├── requirements.txt    # Python dependencies
│   └── .gitignore         # Backend-specific ignores
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and API
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node dependencies
│   └── .gitignore         # Frontend-specific ignores
├── package.json            # Root config (minimal)
├── vercel.json            # Vercel configuration
└── README.md              # This file
```

## 🔑 Environment Variables

### Backend Required

- `GEMINI_API_KEY` - Google Gemini API key
- `TAVILY_API_KEY` - Tavily search API key

### Backend Optional

- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_SECRET` - Reddit API secret
- `REDDIT_USER_AGENT` - Reddit API user agent

### Frontend Required

- `NEXT_PUBLIC_BACKEND_URL` - Backend API URL (auto-configured in single deployment)

## 🚀 Quick Start

### Single Vercel Project (Recommended)

1. **Deploy from root**: `vercel`
2. **Set environment variables** in Vercel dashboard
3. **Test** with a startup idea

### Separate Deployments

1. **Deploy Backend** to Vercel
2. **Deploy Frontend** to Vercel
3. **Set Environment Variables** in both deployments
4. **Test** with a startup idea

## 📊 Analysis Features

- **Market Assessment**: Score, verdict, saturation, barriers, timing
- **Uniqueness Analysis**: Novelty score, differentiation, copycat risk
- **Business Viability**: Market size, monetization, pricing strategy
- **Competitive Landscape**: Existing solutions, gaps, advantages
- **Risk Assessment**: Market, execution, competitive risks
- **Strategic Recommendations**: Entry strategy, next steps, timeline

## 🔒 Security

- CORS enabled for frontend communication
- API key validation
- Input sanitization
- Rate limiting (Vercel built-in)

## 📈 Monitoring

- Health check endpoints
- Service status monitoring
- Error logging and handling
- Performance metrics

## 🆘 Troubleshooting

### Common Issues

1. **"Not Found" Error**: Check API endpoint URLs and Vercel routing
2. **LLM Analysis Fails**: Verify Gemini API key and service availability
3. **File Upload Issues**: Ensure PyPDF2 is installed and working
4. **CORS Errors**: Check CORS configuration in backend

### Debug Steps

1. Check Vercel function logs
2. Verify environment variables
3. Test API endpoints individually
4. Check service health endpoints

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review Vercel deployment logs
3. Open an issue on GitHub

---

**Ready to validate your startup ideas? Deploy and start analyzing! 🚀**
