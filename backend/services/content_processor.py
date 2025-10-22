"""
Content processing service that orchestrates scraping, AI analysis, and storage
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.news_scraper import NewsScraperService, deduplicate_articles, filter_articles
from services.ai_service import AIAnalysisService
from models.database import Article, Theme, Sector, Insight, Trend, TrendDataPoint, Digest
from database.connection import SessionLocal


class ContentProcessor:
    """Main service for processing content pipeline"""

    def __init__(self, api_key: Optional[str] = None):
        self.scraper = NewsScraperService()
        self.ai_service = AIAnalysisService(api_key)

    async def scrape_and_process_all(self) -> Dict:
        """
        Main pipeline: Scrape -> Analyze -> Store
        """
        print("Starting content processing pipeline...")

        # Step 1: Scrape articles
        print("Step 1: Scraping articles from all sources...")
        raw_articles = self.scraper.scrape_all_sources()
        print(f"Scraped {len(raw_articles)} raw articles")

        # Step 2: Deduplicate and filter
        print("Step 2: Filtering and deduplicating...")
        articles = deduplicate_articles(raw_articles)
        articles = filter_articles(articles)
        print(f"After filtering: {len(articles)} unique articles")

        # Step 3: Check which articles are new
        db = SessionLocal()
        try:
            new_articles = self._filter_new_articles(articles, db)
            print(f"New articles to process: {len(new_articles)}")

            if not new_articles:
                print("No new articles to process")
                return {"status": "success", "new_articles": 0}

            # Step 4: AI Analysis
            print("Step 3: Analyzing articles with AI...")
            analyzed_articles = await self._analyze_articles(new_articles)
            print(f"Analyzed {len(analyzed_articles)} articles")

            # Step 5: Store in database
            print("Step 4: Storing articles in database...")
            stored_count = self._store_articles(analyzed_articles, db)
            print(f"Stored {stored_count} articles")

            # Step 6: Extract insights
            print("Step 5: Extracting insights...")
            insights_count = await self._extract_and_store_insights(db)
            print(f"Extracted {insights_count} insights")

            # Step 7: Update trends
            print("Step 6: Updating trends...")
            trends_count = await self._update_trends(db)
            print(f"Updated {trends_count} trends")

            db.commit()

            return {
                "status": "success",
                "new_articles": stored_count,
                "insights": insights_count,
                "trends": trends_count
            }

        except Exception as e:
            db.rollback()
            print(f"Error in processing pipeline: {e}")
            return {"status": "error", "message": str(e)}

        finally:
            db.close()

    def _filter_new_articles(self, articles: List[Dict], db: Session) -> List[Dict]:
        """Filter out articles that already exist in database"""
        existing_urls = set(
            url[0] for url in db.query(Article.url).all()
        )

        new_articles = [
            art for art in articles
            if art.get('url') not in existing_urls
        ]

        return new_articles

    async def _analyze_articles(self, articles: List[Dict]) -> List[Dict]:
        """Analyze articles with AI service"""
        analyzed = []

        # Process in batches
        batch_size = 5
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]

            # Analyze each article in batch
            tasks = [
                self.ai_service.analyze_article(
                    title=art.get('title', ''),
                    content=art.get('content', ''),
                    url=art.get('url', '')
                )
                for art in batch
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Combine original article data with analysis
            for art, analysis in zip(batch, results):
                if isinstance(analysis, Exception):
                    print(f"Error analyzing article: {analysis}")
                    continue

                # Merge analysis results with article
                art.update({
                    'summary': analysis.get('summary'),
                    'key_takeaways': analysis.get('key_takeaways'),
                    'primary_theme': analysis.get('primary_theme'),
                    'secondary_themes': analysis.get('secondary_themes', []),
                    'confidence_score': analysis.get('confidence_score'),
                    'region': analysis.get('region'),
                    'sectors': analysis.get('sectors', []),
                    'sentiment_label': analysis.get('sentiment'),
                    'sentiment_score': analysis.get('sentiment_score'),
                    'signal_strength': analysis.get('signal_strength'),
                    'is_emerging': analysis.get('is_emerging', False),
                })

                analyzed.append(art)

            # Rate limiting
            await asyncio.sleep(1)

        return analyzed

    def _store_articles(self, articles: List[Dict], db: Session) -> int:
        """Store analyzed articles in database"""
        stored_count = 0

        for art_data in articles:
            try:
                # Create article
                article = Article(
                    title=art_data.get('title'),
                    url=art_data.get('url'),
                    source=art_data.get('source'),
                    source_type=art_data.get('source_type'),
                    author=art_data.get('author'),
                    published_date=art_data.get('published_date'),
                    content=art_data.get('content'),
                    summary=art_data.get('summary'),
                    key_takeaways=art_data.get('key_takeaways'),
                    primary_theme=art_data.get('primary_theme'),
                    confidence_score=art_data.get('confidence_score'),
                    region=art_data.get('region'),
                    sentiment_label=art_data.get('sentiment_label'),
                    sentiment_score=art_data.get('sentiment_score'),
                    signal_strength=art_data.get('signal_strength'),
                    is_emerging=art_data.get('is_emerging', False),
                    is_featured=(art_data.get('signal_strength', 0) > 0.8),  # Auto-feature high signal
                )

                db.add(article)
                db.flush()  # Get article ID

                # Add themes
                primary_theme = art_data.get('primary_theme')
                if primary_theme:
                    theme = db.query(Theme).filter(Theme.name == primary_theme).first()
                    if theme:
                        article.themes.append(theme)

                for theme_name in art_data.get('secondary_themes', []):
                    theme = db.query(Theme).filter(Theme.name == theme_name).first()
                    if theme and theme not in article.themes:
                        article.themes.append(theme)

                # Add sectors
                for sector_name in art_data.get('sectors', []):
                    sector = db.query(Sector).filter(Sector.name == sector_name).first()
                    if sector:
                        article.sectors.append(sector)

                stored_count += 1

            except Exception as e:
                print(f"Error storing article {art_data.get('title')}: {e}")
                continue

        return stored_count

    async def _extract_and_store_insights(self, db: Session) -> int:
        """Extract insights from recent articles"""
        # Get articles from last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_articles = db.query(Article)\
            .filter(Article.published_date >= week_ago)\
            .order_by(Article.signal_strength.desc())\
            .limit(20)\
            .all()

        if not recent_articles:
            return 0

        # Prepare article data for AI
        articles_data = [
            {
                'title': art.title,
                'summary': art.summary,
                'primary_theme': art.primary_theme,
            }
            for art in recent_articles
        ]

        # Get insights from AI
        insights = await self.ai_service.extract_insights(articles_data)

        # Store insights
        stored_count = 0
        for insight_data in insights:
            try:
                # Link to most relevant article
                article = recent_articles[0]  # Could improve this matching

                insight = Insight(
                    article_id=article.id,
                    title=insight_data.get('title'),
                    description=insight_data.get('description'),
                    impact_level=insight_data.get('impact_level'),
                    time_horizon=insight_data.get('time_horizon'),
                    relevance_score=insight_data.get('relevance_score'),
                )

                db.add(insight)
                stored_count += 1

            except Exception as e:
                print(f"Error storing insight: {e}")
                continue

        return stored_count

    async def _update_trends(self, db: Session) -> int:
        """Detect and update trends"""
        # Get recent articles
        month_ago = datetime.utcnow() - timedelta(days=30)
        recent_articles = db.query(Article)\
            .filter(Article.published_date >= month_ago)\
            .all()

        if not recent_articles:
            return 0

        # Get existing trend names
        existing_trends = [t.name for t in db.query(Trend.name).all()]

        # Prepare data for AI
        articles_data = [
            {
                'title': art.title,
                'primary_theme': art.primary_theme,
                'published_date': art.published_date,
            }
            for art in recent_articles
        ]

        # Detect new trends
        new_trends = await self.ai_service.detect_emerging_trends(
            articles_data,
            existing_trends
        )

        # Store new trends
        stored_count = 0
        for trend_data in new_trends:
            try:
                # Find theme
                theme = None
                theme_keywords = trend_data.get('keywords', [])
                for kw in theme_keywords:
                    theme = db.query(Theme)\
                        .filter(Theme.keywords.contains([kw]))\
                        .first()
                    if theme:
                        break

                trend = Trend(
                    name=trend_data.get('name'),
                    description=trend_data.get('description'),
                    keywords=trend_data.get('keywords'),
                    theme_id=theme.id if theme else None,
                    start_date=datetime.utcnow(),
                    status=trend_data.get('status', 'emerging'),
                    momentum=trend_data.get('momentum'),
                    region='Global',
                    article_count=0,
                )

                db.add(trend)
                stored_count += 1

            except Exception as e:
                print(f"Error storing trend: {e}")
                continue

        # Update existing trends with new data points
        self._update_trend_data_points(db)

        return stored_count

    def _update_trend_data_points(self, db: Session):
        """Update time-series data for existing trends"""
        trends = db.query(Trend).all()

        for trend in trends:
            # Get articles matching trend keywords
            today = datetime.utcnow().date()

            # Count articles for today
            article_count = 0
            sentiment_total = 0.0
            signal_total = 0.0

            for keyword in trend.keywords or []:
                articles = db.query(Article)\
                    .filter(
                        Article.published_date >= datetime.combine(today, datetime.min.time())
                    )\
                    .filter(
                        (Article.title.contains(keyword)) |
                        (Article.summary.contains(keyword))
                    )\
                    .all()

                article_count += len(articles)
                sentiment_total += sum(a.sentiment_score or 0 for a in articles)
                signal_total += sum(a.signal_strength or 0 for a in articles)

            if article_count > 0:
                # Check if data point for today exists
                existing_dp = db.query(TrendDataPoint)\
                    .filter(
                        TrendDataPoint.trend_id == trend.id,
                        TrendDataPoint.date >= datetime.combine(today, datetime.min.time())
                    )\
                    .first()

                if existing_dp:
                    existing_dp.article_count = article_count
                    existing_dp.sentiment_avg = sentiment_total / article_count
                    existing_dp.signal_strength_avg = signal_total / article_count
                else:
                    dp = TrendDataPoint(
                        trend_id=trend.id,
                        date=datetime.combine(today, datetime.min.time()),
                        article_count=article_count,
                        sentiment_avg=sentiment_total / article_count,
                        signal_strength_avg=signal_total / article_count,
                    )
                    db.add(dp)

                # Update trend metrics
                trend.article_count = article_count
                trend.last_updated = datetime.utcnow()

    async def generate_daily_digest(self, db: Session) -> Optional[Digest]:
        """Generate daily digest"""
        # Get articles from last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        today = datetime.utcnow()

        articles = db.query(Article)\
            .filter(Article.published_date >= yesterday)\
            .order_by(Article.signal_strength.desc())\
            .all()

        if not articles:
            return None

        # Get insights and trends
        insights = db.query(Insight)\
            .filter(Insight.created_date >= yesterday)\
            .order_by(Insight.relevance_score.desc())\
            .limit(5)\
            .all()

        trends = db.query(Trend)\
            .filter(Trend.status == "emerging")\
            .order_by(Trend.momentum.desc())\
            .limit(5)\
            .all()

        # Prepare data for AI digest generation
        articles_data = [
            {
                'title': a.title,
                'summary': a.summary,
                'primary_theme': a.primary_theme,
                'signal_strength': a.signal_strength,
            }
            for a in articles[:15]
        ]

        insights_data = [
            {
                'title': i.title,
                'description': i.description,
                'impact_level': i.impact_level,
            }
            for i in insights
        ]

        trends_data = [
            {
                'name': t.name,
                'description': t.description,
                'momentum': t.momentum,
            }
            for t in trends
        ]

        # Generate digest with AI
        digest_content = await self.ai_service.generate_digest(
            articles_data,
            insights_data,
            trends_data,
            period="daily"
        )

        # Create digest record
        digest = Digest(
            digest_type="daily",
            period_start=yesterday,
            period_end=today,
            title=digest_content.get('title'),
            summary=digest_content.get('summary'),
            top_stories=digest_content.get('top_stories'),
            emerging_trends=[t['name'] for t in trends_data],
            key_insights=digest_content.get('strategic_implications'),
            total_articles=len(articles),
            themes_covered=list(set(a.primary_theme for a in articles if a.primary_theme)),
            regions_covered=list(set(a.region for a in articles if a.region)),
        )

        db.add(digest)
        db.commit()

        return digest


async def run_processing_pipeline():
    """Run the full processing pipeline"""
    processor = ContentProcessor()
    result = await processor.scrape_and_process_all()
    print(f"Processing completed: {result}")


if __name__ == "__main__":
    asyncio.run(run_processing_pipeline())
