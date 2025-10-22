# Quick Start Guide

Get the HR Signals Dashboard up and running in minutes.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## 5-Minute Setup

### 1. Clone and Setup Backend

```bash
cd HR_Signals/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Initialize database
python database/connection.py
```

### 2. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Configure API URL
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python api/main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access the Dashboard

Open your browser to: **http://localhost:3000**

### 5. Load Sample Data

**Terminal 3:**
```bash
cd backend
source venv/bin/activate
python services/content_processor.py
```

This will:
- Scrape latest HR news articles
- Analyze them with AI
- Populate your dashboard with real data

## What's Next?

- **View Articles**: Browse AI-analyzed HR news
- **Check Trends**: See emerging workforce trends
- **Read Insights**: Strategic takeaways for HR leaders
- **Explore Filters**: Filter by theme, region, and sector

## Optional: Automated Updates

To enable automated scraping every 6 hours:

**Terminal 4 - Redis:**
```bash
redis-server
```

**Terminal 5 - Celery Worker:**
```bash
cd backend
celery -A services.tasks worker --loglevel=info
```

**Terminal 6 - Celery Beat:**
```bash
cd backend
celery -A services.tasks beat --loglevel=info
```

## Troubleshooting

**Backend not starting?**
- Check Python version: `python --version` (should be 3.9+)
- Ensure virtual environment is activated
- Verify `.env` file has ANTHROPIC_API_KEY

**Frontend not loading?**
- Check Node version: `node --version` (should be 18+)
- Ensure backend is running on port 8000
- Check browser console for errors

**No articles showing?**
- Run `python services/content_processor.py` to scrape content
- Check internet connection
- Review backend console for error messages

## Configuration

### Add Custom News Sources

Edit `backend/config/settings.py`:

```python
NEWS_SOURCES: dict = {
    "media": [
        "https://www.your-source.com/rss",  # Add your sources here
    ],
}
```

### Adjust AI Model

In `.env`:
```bash
AI_MODEL=claude-3-5-sonnet-20241022  # or another Claude model
```

### Change Themes

Edit `backend/database/connection.py` in the `seed_initial_data()` function.

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review error logs in the terminal
- Ensure all prerequisites are installed

Enjoy your HR Signals Dashboard!
