"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "HR Signals Dashboard"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./hr_signals.db"

    # AI Services
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "claude-3-5-sonnet-20241022"  # Default to Claude

    # Scraping
    USER_AGENT: str = "HR-Signals-Bot/1.0"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    # Celery/Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Content Processing
    MAX_SUMMARY_LENGTH: int = 500
    MIN_CONTENT_LENGTH: int = 100

    # Filtering
    ALLOWED_LANGUAGES: List[str] = ["en"]

    # Geographic regions
    REGIONS: List[str] = ["Global", "Australia", "Asia Pacific", "North America", "Europe", "UK"]

    # Themes
    THEMES: List[str] = [
        "Workforce Transformation",
        "AI Governance",
        "Skills and Capability",
        "HR Technology",
        "Policy and Regulation",
        "Future of Work",
        "Employee Experience",
        "Talent Acquisition",
        "Diversity and Inclusion",
        "Organizational Culture"
    ]

    # Sectors
    SECTORS: List[str] = [
        "Technology",
        "Financial Services",
        "Healthcare",
        "Manufacturing",
        "Retail",
        "Professional Services",
        "Public Sector",
        "Education",
        "Energy",
        "General"
    ]

    # News Sources
    NEWS_SOURCES: dict = {
        "consulting_firms": [
            "https://www.mckinsey.com/featured-insights/rss/future-of-work",
            "https://www.bcg.com/rss/featured-insights.rss",
            "https://www.pwc.com/gx/en/services/people-organisation/rss.xml",
            "https://www2.deloitte.com/us/en/insights/focus/human-capital-trends.html",
        ],
        "media": [
            "https://www.hrdive.com/feeds/news/",
            "https://www.shrm.org/resourcesandtools/hr-topics/pages/default.aspx",
            "https://www.hcamag.com/au/rss",
            "https://www.hrmorning.com/feed/",
        ],
        "hr_tech": [
            "https://www.hrtechnologist.com/feed/",
            "https://www.peoplemanagementmagazine.com/feed/",
        ],
        "research": [
            "https://www.gartner.com/en/newsroom/rss",
            "https://www.forrester.com/rss/",
        ]
    }

    # Update frequencies
    SCRAPE_INTERVAL_HOURS: int = 6
    DIGEST_DAILY_TIME: str = "08:00"  # 8 AM
    DIGEST_WEEKLY_DAY: int = 1  # Monday

    # Trend Detection
    TREND_LOOKBACK_DAYS: int = 30
    EMERGING_TOPIC_THRESHOLD: float = 0.7  # Similarity threshold
    SIGNAL_STRENGTH_WINDOW: int = 7  # Days

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
