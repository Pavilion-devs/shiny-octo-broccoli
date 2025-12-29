# Deploying CRAG to Render

## Prerequisites
1. GitHub account (to push your code)
2. Render account (free tier available at render.com)
3. OpenAI API key
4. Brave Search API key

## Step 1: Prepare Your Repository

### Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - CRAG app ready for deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Important Files for Render:
- ✅ `requirements.txt` - Already cleaned up and ready
- ✅ `chainlit_app.py` - Your main application file
- ✅ `.env` - DO NOT commit this file (add to .gitignore)

## Step 2: Create .gitignore (if not exists)

Create a `.gitignore` file with:
```
.env
myenv/
venv/
__pycache__/
*.pyc
.DS_Store
vectorstore/
data/
```

## Step 3: Deploy on Render

### Option A: Deploy as Web Service (Recommended)

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com/
   - Click "New +" → "Web Service"

2. **Connect GitHub Repository**
   - Select your CRAG repository
   - Give it a name (e.g., `mobolaji-crag-app`)

3. **Configure Settings**
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `chainlit run chainlit_app.py --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (or paid for better performance)

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   - `OPENAI_API_KEY` = your-openai-key
   - `BRAVE_API_KEY` = your-brave-key
   - `TOKENIZERS_PARALLELISM` = false

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

### Option B: Deploy Using Dockerfile (Alternative)

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run chainlit
CMD ["chainlit", "run", "chainlit_app.py", "--host", "0.0.0.0", "--port", "8000"]
```

Then on Render:
- Choose "Docker" as environment
- Build Command: (leave empty)
- Start Command: (leave empty, uses CMD from Dockerfile)

## Step 4: Handle Data Files

**Important:** The `data/` folder with PDFs won't be included in deployment (it's in .gitignore).

Options:
1. **Remove from .gitignore** if PDFs are public/non-sensitive
2. **Use cloud storage** (AWS S3, Google Cloud Storage) and download at startup
3. **Upload via admin interface** (requires additional code)

## Step 5: Post-Deployment Checklist

- [ ] Test the deployed URL
- [ ] Verify API keys are working (check logs)
- [ ] Test document retrieval
- [ ] Test web search fallback
- [ ] Monitor logs for errors

## Troubleshooting

### If build fails:
- Check Python version (should be 3.12)
- Review build logs on Render dashboard
- Ensure all dependencies in requirements.txt are correct

### If app crashes on startup:
- Check environment variables are set
- Review application logs
- Ensure PORT environment variable is used

### Memory issues:
- Upgrade to paid tier (512 MB free tier might be tight)
- Or optimize by using smaller embedding models

## Alternative: Deploy to Other Platforms

### Heroku:
Create `Procfile`:
```
web: chainlit run chainlit_app.py --host 0.0.0.0 --port $PORT
```

### Railway:
- Similar to Render
- Connect GitHub repo
- Add environment variables
- Deploy automatically

### Google Cloud Run / AWS Elastic Beanstalk:
- Use the Dockerfile approach
- Configure environment variables in platform settings

## Cost Considerations

- **Render Free Tier:** Limited to 750 hours/month, sleeps after inactivity
- **Render Paid:** Starting at $7/month for always-on service
- **OpenAI Costs:** Pay per token usage
- **Brave Search:** Free tier available

## Support

Built by MOBOLAJI OPEYEMI BOLATITO OBINNA
CRAG System (Corrective Retrieval-Augmented Generation)

