# 🚀 Deployment Guide - Startup Guillotine

This guide will help you deploy the Startup Guillotine monorepo to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: For repository hosting
3. **API Keys**:
   - Google AI Studio API Key (Gemini)
   - Tavily API Key

## 🔑 API Keys Setup

### 1. Google AI Studio (Gemini)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for later use

### 2. Tavily API

1. Go to [Tavily](https://tavily.com)
2. Sign up for a free account
3. Get your API key from the dashboard

## 🏗️ Vercel Deployment

### Option 1: Deploy via Vercel Dashboard

1. **Push to GitHub**

   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**

   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Select the repository

3. **Configure Build Settings**

   - **Framework Preset**: Other
   - **Root Directory**: `./` (root of monorepo)
   - **Build Command**: `npm run build`
   - **Output Directory**: `frontend/.next`
   - **Install Command**: `npm run install:all`

4. **Environment Variables (CRITICAL)**
   **Set these in the Vercel dashboard under Project Settings → Environment Variables:**

   ```
   GOOGLE_AI_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   CORS_ORIGINS=https://your-domain.vercel.app
   NEXT_PUBLIC_BACKEND_URL=https://your-domain.vercel.app
   ```

   **Important Notes:**

   - These variables are available to both frontend and backend
   - `NEXT_PUBLIC_` prefix makes variables available to client-side code
   - Update `CORS_ORIGINS` with your actual Vercel domain after deployment

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**

   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**

   ```bash
   vercel login
   ```

3. **Deploy**

   ```bash
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add GOOGLE_AI_API_KEY
   vercel env add TAVILY_API_KEY
   vercel env add CORS_ORIGINS
   vercel env add NEXT_PUBLIC_BACKEND_URL
   ```

## 🔧 Configuration Files

### vercel.json (Root)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

## 🏠 Local Development

For local development, create a `.env` file in the root directory:

```bash
# .env (root directory)
GOOGLE_AI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**

   - Check if all dependencies are installed
   - Verify API keys are set correctly in Vercel dashboard
   - Check build logs in Vercel dashboard

2. **API Errors**

   - Verify CORS settings
   - Check if backend is accessible
   - Test API endpoints directly
   - Ensure environment variables are set in Vercel dashboard

3. **File Upload Issues**

   - Check file size limits
   - Verify file type restrictions
   - Test with different file formats

4. **Environment Variable Issues**
   - Ensure variables are set in Vercel dashboard (not in local .env files)
   - Check variable names match exactly
   - Redeploy after adding new environment variables

### Debug Commands

```bash
# Test backend locally
cd backend
python -m uvicorn main:app --reload

# Test frontend locally
cd frontend
npm run dev

# Check API health
curl https://your-domain.vercel.app/api/health
```

## 📊 Monitoring

### Vercel Analytics

- Enable Vercel Analytics in dashboard
- Monitor performance and errors
- Track API usage

### Logs

- Check Vercel function logs
- Monitor API response times
- Track error rates

## 🔄 Updates

### Deploy Updates

```bash
git add .
git commit -m "Update description"
git push origin main
# Vercel will auto-deploy
```

### Environment Variable Updates

- Go to Vercel dashboard
- Project Settings → Environment Variables
- Update values and redeploy

## 🛡️ Security

### Best Practices

1. Never commit API keys to Git
2. Use Vercel environment variables (not local .env files)
3. Enable CORS properly
4. Validate file uploads
5. Rate limit API calls

### API Key Rotation

1. Generate new API keys
2. Update Vercel environment variables
3. Redeploy application
4. Revoke old keys

## 📞 Support

If you encounter issues:

1. Check Vercel documentation
2. Review build logs
3. Test locally first
4. Contact support if needed

---

**Happy Deploying! 🎉**
