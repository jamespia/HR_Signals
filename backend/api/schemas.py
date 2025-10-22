"""
Pydantic schemas for API request/response models
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Article schemas
class ThemeBase(BaseModel):
    id: int
    name: str
    color: Optional[str] = None

    class Config:
        from_attributes = True


class SectorBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    source: str
    source_type: Optional[str] = None
    author: Optional[str] = None
    published_date: datetime
    scraped_date: datetime

    summary: Optional[str] = None
    key_takeaways: Optional[List[str]] = None

    primary_theme: Optional[str] = None
    confidence_score: Optional[float] = None
    region: Optional[str] = None

    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    signal_strength: Optional[float] = None

    is_featured: bool = False
    is_emerging: bool = False
    view_count: int = 0

    themes: List[ThemeBase] = []
    sectors: List[SectorBase] = []

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    title: str
    url: HttpUrl
    source: str
    source_type: Optional[str] = None
    author: Optional[str] = None
    published_date: datetime
    content: Optional[str] = None


class ArticleFilterParams(BaseModel):
    theme: Optional[str] = None
    sector: Optional[str] = None
    region: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search: Optional[str] = None
    is_featured: Optional[bool] = None
    min_signal_strength: Optional[float] = None


# Theme schemas
class ThemeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True


# Sector schemas
class SectorResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Insight schemas
class InsightResponse(BaseModel):
    id: int
    article_id: int
    title: str
    description: str
    impact_level: Optional[str] = None
    time_horizon: Optional[str] = None
    created_date: datetime
    relevance_score: Optional[float] = None

    class Config:
        from_attributes = True


class InsightCreate(BaseModel):
    article_id: int
    title: str
    description: str
    impact_level: Optional[str] = None
    time_horizon: Optional[str] = None
    relevance_score: Optional[float] = None


# Trend schemas
class TrendDataPointResponse(BaseModel):
    date: datetime
    article_count: int
    sentiment_avg: Optional[float] = None
    signal_strength_avg: Optional[float] = None

    class Config:
        from_attributes = True


class TrendResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    start_date: datetime
    last_updated: datetime
    article_count: int
    momentum: Optional[float] = None
    status: Optional[str] = None
    region: Optional[str] = None
    data_points: List[TrendDataPointResponse] = []

    class Config:
        from_attributes = True


class TrendCreate(BaseModel):
    name: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    theme_id: Optional[int] = None
    status: Optional[str] = "emerging"
    region: Optional[str] = "Global"


# Digest schemas
class DigestResponse(BaseModel):
    id: int
    digest_type: str
    period_start: datetime
    period_end: datetime
    created_date: datetime
    title: Optional[str] = None
    summary: Optional[str] = None
    top_stories: Optional[List[Any]] = None
    emerging_trends: Optional[List[str]] = None
    key_insights: Optional[List[Any]] = None
    total_articles: Optional[int] = None
    themes_covered: Optional[List[str]] = None
    regions_covered: Optional[List[str]] = None

    class Config:
        from_attributes = True


class DigestCreate(BaseModel):
    digest_type: str
    period_start: datetime
    period_end: datetime
    title: Optional[str] = None
    summary: Optional[str] = None


# Stats schemas
class ThemeDistribution(BaseModel):
    theme: str
    count: int


class SentimentDistribution(BaseModel):
    sentiment: str
    count: int


class StatsResponse(BaseModel):
    total_articles: int
    recent_articles: int
    total_insights: int
    total_trends: int
    emerging_trends: int
    theme_distribution: List[ThemeDistribution]
    sentiment_distribution: List[SentimentDistribution]


# Processing schemas
class ProcessingJob(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    articles_processed: int = 0
    errors: List[str] = []


# User action schemas
class BulkArticleAction(BaseModel):
    article_ids: List[int]
    action: str  # feature, archive, delete


# Filter presets
class FilterPreset(BaseModel):
    name: str
    filters: ArticleFilterParams
    is_default: bool = False
