"""
Database models for HR Signals Dashboard
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association tables for many-to-many relationships
article_themes = Table(
    'article_themes',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('theme_id', Integer, ForeignKey('themes.id'))
)

article_sectors = Table(
    'article_sectors',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('sector_id', Integer, ForeignKey('sectors.id'))
)


class Article(Base):
    """News article model"""
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False, index=True)
    source = Column(String(200), nullable=False)
    source_type = Column(String(100))  # consulting_firm, media, hr_tech, research
    author = Column(String(200))
    published_date = Column(DateTime, nullable=False, index=True)
    scraped_date = Column(DateTime, default=datetime.utcnow)

    # Content
    content = Column(Text)
    summary = Column(Text)
    key_takeaways = Column(JSON)  # List of key points

    # Classification
    primary_theme = Column(String(100))
    confidence_score = Column(Float)  # AI classification confidence
    region = Column(String(100), index=True)
    language = Column(String(10), default='en')

    # Analysis
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String(50))  # positive, negative, neutral
    signal_strength = Column(Float)  # 0 to 1 - importance/impact score

    # Metadata
    is_featured = Column(Boolean, default=False)
    is_emerging = Column(Boolean, default=False)  # Emerging trend flag
    view_count = Column(Integer, default=0)

    # Relationships
    themes = relationship("Theme", secondary=article_themes, back_populates="articles")
    sectors = relationship("Sector", secondary=article_sectors, back_populates="articles")
    insights = relationship("Insight", back_populates="article")


class Theme(Base):
    """Theme/category model"""
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    keywords = Column(JSON)  # List of keywords for classification
    color = Column(String(20))  # For UI visualization

    # Relationships
    articles = relationship("Article", secondary=article_themes, back_populates="themes")
    trends = relationship("Trend", back_populates="theme")


class Sector(Base):
    """Industry sector model"""
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)

    # Relationships
    articles = relationship("Article", secondary=article_sectors, back_populates="sectors")


class Insight(Base):
    """Extracted insights from articles"""
    __tablename__ = 'insights'

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)

    # Insight content
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    impact_level = Column(String(50))  # high, medium, low
    time_horizon = Column(String(50))  # immediate, short-term, long-term

    # Metadata
    created_date = Column(DateTime, default=datetime.utcnow)
    relevance_score = Column(Float)

    # Relationships
    article = relationship("Article", back_populates="insights")


class Trend(Base):
    """Detected trends over time"""
    __tablename__ = 'trends'

    id = Column(Integer, primary_key=True, index=True)
    theme_id = Column(Integer, ForeignKey('themes.id'))

    # Trend data
    name = Column(String(200), nullable=False)
    description = Column(Text)
    keywords = Column(JSON)  # Keywords associated with trend

    # Metrics
    start_date = Column(DateTime, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
    article_count = Column(Integer, default=0)
    momentum = Column(Float)  # Growth rate
    peak_date = Column(DateTime)

    # Classification
    status = Column(String(50))  # emerging, growing, peak, declining
    region = Column(String(100))

    # Relationships
    theme = relationship("Theme", back_populates="trends")
    data_points = relationship("TrendDataPoint", back_populates="trend")


class TrendDataPoint(Base):
    """Time-series data points for trends"""
    __tablename__ = 'trend_data_points'

    id = Column(Integer, primary_key=True, index=True)
    trend_id = Column(Integer, ForeignKey('trends.id'), nullable=False)

    date = Column(DateTime, nullable=False, index=True)
    article_count = Column(Integer, default=0)
    sentiment_avg = Column(Float)
    signal_strength_avg = Column(Float)

    # Relationships
    trend = relationship("Trend", back_populates="data_points")


class Digest(Base):
    """Daily/Weekly digest summaries"""
    __tablename__ = 'digests'

    id = Column(Integer, primary_key=True, index=True)

    # Digest metadata
    digest_type = Column(String(20), nullable=False)  # daily, weekly
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Content
    title = Column(String(300))
    summary = Column(Text)
    top_stories = Column(JSON)  # List of article IDs
    emerging_trends = Column(JSON)  # List of trend names
    key_insights = Column(JSON)  # List of insight summaries

    # Metrics
    total_articles = Column(Integer)
    themes_covered = Column(JSON)
    regions_covered = Column(JSON)


class Source(Base):
    """News source tracking"""
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    source_type = Column(String(100))  # consulting_firm, media, hr_tech, research

    # Scraping metadata
    last_scraped = Column(DateTime)
    scrape_frequency_hours = Column(Integer, default=6)
    is_active = Column(Boolean, default=True)

    # Quality metrics
    article_count = Column(Integer, default=0)
    avg_signal_strength = Column(Float)
    reliability_score = Column(Float)


class SearchQuery(Base):
    """Saved search queries and alerts"""
    __tablename__ = 'search_queries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    query = Column(Text, nullable=False)

    # Filters
    themes = Column(JSON)
    sectors = Column(JSON)
    regions = Column(JSON)
    date_from = Column(DateTime)
    date_to = Column(DateTime)

    # Alert settings
    is_alert = Column(Boolean, default=False)
    alert_frequency = Column(String(50))  # daily, weekly
    last_sent = Column(DateTime)

    created_date = Column(DateTime, default=datetime.utcnow)
