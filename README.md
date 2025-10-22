# HR Signals Dashboard

An AI-powered intelligence platform that automatically scans, curates, and summarizes the most relevant, high-impact stories in HR, workforce, and AI-in-work domains. This system serves as a command centre for HR and transformation leaders, turning external noise into actionable foresight.

## Features

### Core Capabilities

- **Automated Content Aggregation**: Scrapes news from global and Australian sources including:
  - Consulting firms (McKinsey, BCG, PwC, Deloitte)
  - Media outlets (HR Dive, SHRM, HCA Magazine)
  - HR tech vendors and industry publications
  - Research institutes and think tanks

- **AI-Powered Analysis**: Uses Claude 3.5 Sonnet for:
  - Executive-ready article summarization
  - Key takeaway extraction
  - Theme classification and categorization
  - Sentiment analysis
  - Signal strength assessment
  - Emerging trend detection

- **Intelligent Classification**: Content organized by:
  - **Themes**: Workforce Transformation, AI Governance, Skills & Capability, HR Technology, Policy & Regulation, Future of Work, Employee Experience, Talent Acquisition, Diversity & Inclusion, Organizational Culture
  - **Geographic Regions**: Global, Australia, Asia Pacific, North America, Europe, UK
  - **Industry Sectors**: Technology, Financial Services, Healthcare, Manufacturing, Retail, Professional Services, Public Sector, Education, Energy

- **Trend Detection**:
  - Identifies emerging topics before mainstream coverage
  - Tracks trend momentum and growth
  - Visualizes trend evolution over time
  - Signal strength metrics

- **Insights Extraction**:
  - Cross-cutting insights from multiple articles
  - Impact level assessment (high/medium/low)
  - Time horizon classification (immediate/short-term/long-term)
  - Strategic implications for HR leaders

- **Daily/Weekly Digests**:
  - Auto-generated executive summaries
  - Top stories highlighting
  - Emerging trend alerts
  - Strategic recommendations

- **Advanced Filtering**:
  - Filter by theme, sector, region
  - Signal strength filtering
  - Featured content
  - Emerging trends
  - Full-text search

- **Rich Visualizations**:
  - Theme distribution charts
  - Sentiment analysis
  - Trend line graphs
  - Signal strength indicators
  - Activity metrics

## Architecture

### Backend (Python/FastAPI)
- **API Layer**: RESTful API with FastAPI
- **Database**: SQLAlchemy ORM with SQLite (upgradable to PostgreSQL)
- **AI Service**: Anthropic Claude API integration
- **Scraping**: BeautifulSoup, Scrapy, Newspaper3k
- **Task Queue**: Celery with Redis for scheduled jobs
- **Processing Pipeline**: Automated scraping → AI analysis → Storage → Insights

### Frontend (React/TypeScript)
- **Framework**: React 18 with TypeScript
- **Routing**: React Router v6
- **State Management**: React Query + Zustand
- **UI Components**: Tailwind CSS + Headless UI
- **Charts**: Recharts for data visualization
- **Build Tool**: Vite

## Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- Redis (for scheduled tasks)
- Anthropic API key

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd HR_Signals
```

2. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp ../.env.example .env
# Edit .env and add your Anthropic API key
```

5. **Initialize database**
```bash
python database/connection.py
```

6. **Start the backend server**
```bash
python api/main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create environment file**
```bash
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
```

4. **Start development server**
```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

### Scheduled Tasks Setup (Optional)

For automated content scraping and digest generation:

1. **Start Redis**
```bash
redis-server
```

2. **Start Celery worker**
```bash
cd backend
celery -A services.tasks worker --loglevel=info
```

3. **Start Celery beat (scheduler)**
```bash
celery -A services.tasks beat --loglevel=info
```

## Usage

### Manual Content Processing

Run the scraping and analysis pipeline manually:

```bash
cd backend
python services/content_processor.py
```

This will:
1. Scrape articles from all configured sources
2. Analyze content with AI
3. Extract themes, sentiments, and insights
4. Store in database
5. Detect emerging trends

### API Endpoints

#### Articles
- `GET /api/v1/articles` - Get all articles with filtering
- `GET /api/v1/articles/{id}` - Get single article
- `GET /api/v1/articles/featured` - Get featured articles

#### Themes
- `GET /api/v1/themes` - Get all themes
- `GET /api/v1/themes/{id}/articles` - Get articles by theme

#### Trends
- `GET /api/v1/trends` - Get all trends
- `GET /api/v1/trends/emerging` - Get emerging trends

#### Insights
- `GET /api/v1/insights` - Get all insights

#### Digests
- `GET /api/v1/digests` - Get all digests
- `GET /api/v1/digests/latest` - Get latest digest

#### Search
- `GET /api/v1/search?q={query}` - Search across content

#### Stats
- `GET /api/v1/stats` - Get dashboard statistics

### Dashboard Features

1. **Command Centre (Home)**
   - Overview statistics
   - Featured stories
   - Emerging trends
   - High-impact insights
   - Theme distribution
   - Sentiment analysis

2. **Articles Page**
   - Filterable article list
   - Theme, region, sector filters
   - Signal strength filtering
   - Search functionality
   - Pagination

3. **Article Detail**
   - Full article information
   - AI-generated summary
   - Key takeaways
   - Sentiment and signal metrics
   - Related themes and sectors
   - Link to original source

4. **Trends Page**
   - Trend tracking
   - Momentum indicators
   - Time-series visualizations
   - Trend status (emerging/growing/peak/declining)

5. **Insights Page**
   - Strategic insights
   - Impact level indicators
   - Time horizon classification
   - Relevance scoring

6. **Digests Page**
   - Daily and weekly summaries
   - Top stories
   - Emerging trend alerts
   - Strategic implications

## Configuration

### News Sources

Configure sources in `backend/config/settings.py`:

```python
NEWS_SOURCES: dict = {
    "consulting_firms": [
        "https://www.mckinsey.com/featured-insights/rss/future-of-work",
        # Add more sources...
    ],
    "media": [
        "https://www.hrdive.com/feeds/news/",
        # Add more sources...
    ],
    # ...
}
```

### Themes and Sectors

Themes and sectors are seeded automatically. To customize, edit the `seed_initial_data()` function in `backend/database/connection.py`.

### AI Model

Change the AI model in `.env`:

```bash
AI_MODEL=claude-3-5-sonnet-20241022
```

### Scheduled Tasks

Adjust scraping and digest schedules in `backend/services/tasks.py`:

```python
celery_app.conf.beat_schedule = {
    'scrape-every-6-hours': {
        'task': 'scrape_and_process_content',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    # ...
}
```

## Data Model

### Key Tables

- **Articles**: News articles with content, metadata, and AI analysis
- **Themes**: Classification categories
- **Sectors**: Industry sectors
- **Insights**: Extracted strategic insights
- **Trends**: Detected trends with time-series data
- **Digests**: Generated daily/weekly summaries
- **Sources**: News source tracking

### Relationships

- Articles ↔ Themes (many-to-many)
- Articles ↔ Sectors (many-to-many)
- Articles → Insights (one-to-many)
- Themes → Trends (one-to-many)
- Trends → TrendDataPoints (one-to-many)

## Development

### Adding New News Sources

1. Add RSS feed or webpage URL to `NEWS_SOURCES` in `backend/config/settings.py`
2. For complex sources, create custom scraper in `backend/scrapers/news_scraper.py`

### Customizing AI Analysis

Edit prompts in `backend/services/ai_service.py`:
- `analyze_article()` - Article analysis
- `extract_insights()` - Insight extraction
- `detect_emerging_trends()` - Trend detection
- `generate_digest()` - Digest generation

### Adding New Themes

Add to database via migration or manual insertion:

```python
theme = Theme(
    name="New Theme",
    description="Description",
    keywords=["keyword1", "keyword2"],
    color="#3B82F6"
)
db.add(theme)
db.commit()
```

## Deployment

### Production Considerations

1. **Database**: Migrate to PostgreSQL
   ```bash
   DATABASE_URL=postgresql://user:password@localhost/hr_signals
   ```

2. **API Server**: Use Gunicorn
   ```bash
   gunicorn backend.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Frontend**: Build for production
   ```bash
   cd frontend
   npm run build
   ```

4. **Environment Variables**: Set in production environment
   - `ANTHROPIC_API_KEY`
   - `DATABASE_URL`
   - `CELERY_BROKER_URL`
   - `DEBUG=False`

5. **CORS**: Update allowed origins in `backend/api/main.py`

6. **Rate Limiting**: Implement API rate limiting

7. **Caching**: Add Redis caching for API responses

8. **Monitoring**: Set up logging and error tracking

## Project Structure

```
HR_Signals/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   └── schemas.py           # Pydantic schemas
│   ├── config/
│   │   └── settings.py          # Configuration
│   ├── database/
│   │   └── connection.py        # Database setup
│   ├── models/
│   │   └── database.py          # SQLAlchemy models
│   ├── scrapers/
│   │   └── news_scraper.py      # Web scraping logic
│   ├── services/
│   │   ├── ai_service.py        # AI analysis
│   │   ├── content_processor.py # Processing pipeline
│   │   └── tasks.py             # Celery tasks
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.tsx       # Main layout
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx    # Home page
│   │   │   ├── ArticlesPage.tsx # Articles list
│   │   │   ├── ArticleDetail.tsx# Article view
│   │   │   ├── TrendsPage.tsx   # Trends
│   │   │   ├── InsightsPage.tsx # Insights
│   │   │   └── DigestsPage.tsx  # Digests
│   │   ├── services/
│   │   │   └── api.ts           # API client
│   │   ├── App.tsx              # Root component
│   │   └── main.tsx             # Entry point
│   ├── package.json             # Node dependencies
│   └── vite.config.ts           # Vite config
├── .env.example                 # Environment template
├── .gitignore
└── README.md
```

## Troubleshooting

### Common Issues

1. **No articles scraped**
   - Check internet connection
   - Verify RSS feed URLs are accessible
   - Check logs for scraping errors

2. **AI analysis failing**
   - Verify Anthropic API key is correct
   - Check API quota/rate limits
   - Review error logs

3. **Frontend not connecting to backend**
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify API URL in frontend `.env`

4. **Celery tasks not running**
   - Ensure Redis is running
   - Check Celery worker is started
   - Verify Celery beat is running

## Future Enhancements

- [ ] Email digest delivery
- [ ] Custom alert configuration
- [ ] Multi-user support with authentication
- [ ] Saved searches and filters
- [ ] Export to PDF/Excel
- [ ] Integration with Slack/Teams
- [ ] Mobile responsive improvements
- [ ] Advanced NLP for entity extraction
- [ ] Competitive intelligence tracking
- [ ] Integration with internal HR systems
- [ ] Browser extension for one-click article saving
- [ ] API webhooks for real-time updates

## License

MIT License - feel free to use and modify for your organization's needs.

## Contributing

Contributions welcome! Please submit pull requests or open issues for bugs and feature requests.