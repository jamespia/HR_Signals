"""
Main FastAPI application for HR Signals Dashboard
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from database.connection import get_db, init_db, seed_initial_data
from models.database import (
    Article, Theme, Sector, Insight, Trend, Digest, Source, TrendDataPoint
)
from api.schemas import (
    ArticleResponse, ThemeResponse, SectorResponse, InsightResponse,
    TrendResponse, DigestResponse, ArticleFilterParams, StatsResponse
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered HR News and Insights Dashboard"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    seed_initial_data()


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.APP_VERSION}


# Articles endpoints
@app.get(f"{settings.API_V1_PREFIX}/articles", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = 0,
    limit: int = 20,
    theme: Optional[str] = None,
    sector: Optional[str] = None,
    region: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    search: Optional[str] = None,
    is_featured: Optional[bool] = None,
    is_emerging: Optional[bool] = None,
    min_signal_strength: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Get articles with filtering options
    """
    query = db.query(Article)

    # Apply filters
    if theme:
        query = query.join(Article.themes).filter(Theme.name == theme)

    if sector:
        query = query.join(Article.sectors).filter(Sector.name == sector)

    if region:
        query = query.filter(Article.region == region)

    if start_date:
        query = query.filter(Article.published_date >= start_date)

    if end_date:
        query = query.filter(Article.published_date <= end_date)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Article.title.ilike(search_term)) |
            (Article.summary.ilike(search_term))
        )

    if is_featured is not None:
        query = query.filter(Article.is_featured == is_featured)

    if is_emerging is not None:
        query = query.filter(Article.is_emerging == is_emerging)

    if min_signal_strength:
        query = query.filter(Article.signal_strength >= min_signal_strength)

    # Order by date, newest first
    query = query.order_by(Article.published_date.desc())

    # Pagination
    articles = query.offset(skip).limit(limit).all()

    return articles


@app.get(f"{settings.API_V1_PREFIX}/articles/{{article_id}}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get single article by ID"""
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Increment view count
    article.view_count += 1
    db.commit()

    return article


@app.get(f"{settings.API_V1_PREFIX}/articles/featured", response_model=List[ArticleResponse])
async def get_featured_articles(limit: int = 10, db: Session = Depends(get_db)):
    """Get featured articles"""
    articles = db.query(Article)\
        .filter(Article.is_featured == True)\
        .order_by(Article.published_date.desc())\
        .limit(limit)\
        .all()

    return articles


# Themes endpoints
@app.get(f"{settings.API_V1_PREFIX}/themes", response_model=List[ThemeResponse])
async def get_themes(db: Session = Depends(get_db)):
    """Get all themes"""
    themes = db.query(Theme).all()
    return themes


@app.get(f"{settings.API_V1_PREFIX}/themes/{{theme_id}}/articles", response_model=List[ArticleResponse])
async def get_theme_articles(
    theme_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get articles for a specific theme"""
    theme = db.query(Theme).filter(Theme.id == theme_id).first()

    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    articles = db.query(Article)\
        .join(Article.themes)\
        .filter(Theme.id == theme_id)\
        .order_by(Article.published_date.desc())\
        .limit(limit)\
        .all()

    return articles


# Insights endpoints
@app.get(f"{settings.API_V1_PREFIX}/insights", response_model=List[InsightResponse])
async def get_insights(
    skip: int = 0,
    limit: int = 20,
    impact_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get insights"""
    query = db.query(Insight)

    if impact_level:
        query = query.filter(Insight.impact_level == impact_level)

    insights = query.order_by(Insight.relevance_score.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

    return insights


# Trends endpoints
@app.get(f"{settings.API_V1_PREFIX}/trends", response_model=List[TrendResponse])
async def get_trends(
    status: Optional[str] = None,
    theme_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get trends"""
    query = db.query(Trend)

    if status:
        query = query.filter(Trend.status == status)

    if theme_id:
        query = query.filter(Trend.theme_id == theme_id)

    trends = query.order_by(Trend.momentum.desc()).all()

    return trends


@app.get(f"{settings.API_V1_PREFIX}/trends/emerging", response_model=List[TrendResponse])
async def get_emerging_trends(limit: int = 10, db: Session = Depends(get_db)):
    """Get emerging trends"""
    trends = db.query(Trend)\
        .filter(Trend.status == "emerging")\
        .order_by(Trend.momentum.desc())\
        .limit(limit)\
        .all()

    return trends


# Digests endpoints
@app.get(f"{settings.API_V1_PREFIX}/digests", response_model=List[DigestResponse])
async def get_digests(
    digest_type: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get digests"""
    query = db.query(Digest)

    if digest_type:
        query = query.filter(Digest.digest_type == digest_type)

    digests = query.order_by(Digest.created_date.desc()).limit(limit).all()

    return digests


@app.get(f"{settings.API_V1_PREFIX}/digests/latest", response_model=DigestResponse)
async def get_latest_digest(
    digest_type: str = "daily",
    db: Session = Depends(get_db)
):
    """Get latest digest"""
    digest = db.query(Digest)\
        .filter(Digest.digest_type == digest_type)\
        .order_by(Digest.created_date.desc())\
        .first()

    if not digest:
        raise HTTPException(status_code=404, detail="No digest found")

    return digest


# Stats endpoint
@app.get(f"{settings.API_V1_PREFIX}/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    # Get counts
    total_articles = db.query(Article).count()
    total_insights = db.query(Insight).count()
    total_trends = db.query(Trend).count()

    # Get recent articles (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_articles = db.query(Article)\
        .filter(Article.published_date >= week_ago)\
        .count()

    # Get emerging trends count
    emerging_trends = db.query(Trend)\
        .filter(Trend.status == "emerging")\
        .count()

    # Get theme distribution
    from sqlalchemy import func
    theme_distribution = db.query(
        Theme.name,
        func.count(Article.id).label('count')
    ).join(Article.themes)\
        .group_by(Theme.name)\
        .order_by(func.count(Article.id).desc())\
        .limit(10)\
        .all()

    # Get sentiment distribution
    sentiment_distribution = db.query(
        Article.sentiment_label,
        func.count(Article.id).label('count')
    ).filter(Article.sentiment_label.isnot(None))\
        .group_by(Article.sentiment_label)\
        .all()

    return {
        "total_articles": total_articles,
        "recent_articles": recent_articles,
        "total_insights": total_insights,
        "total_trends": total_trends,
        "emerging_trends": emerging_trends,
        "theme_distribution": [
            {"theme": t[0], "count": t[1]}
            for t in theme_distribution
        ],
        "sentiment_distribution": [
            {"sentiment": s[0], "count": s[1]}
            for s in sentiment_distribution
        ]
    }


# Search endpoint
@app.get(f"{settings.API_V1_PREFIX}/search")
async def search_content(
    q: str = Query(..., min_length=2),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search articles, insights, and trends"""
    search_term = f"%{q}%"

    # Search articles
    articles = db.query(Article)\
        .filter(
            (Article.title.ilike(search_term)) |
            (Article.summary.ilike(search_term))
        )\
        .order_by(Article.published_date.desc())\
        .limit(limit)\
        .all()

    # Search insights
    insights = db.query(Insight)\
        .filter(
            (Insight.title.ilike(search_term)) |
            (Insight.description.ilike(search_term))
        )\
        .limit(limit)\
        .all()

    # Search trends
    trends = db.query(Trend)\
        .filter(
            (Trend.name.ilike(search_term)) |
            (Trend.description.ilike(search_term))
        )\
        .limit(limit)\
        .all()

    return {
        "articles": articles,
        "insights": insights,
        "trends": trends,
        "total_results": len(articles) + len(insights) + len(trends)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
