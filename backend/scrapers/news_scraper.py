"""
News scraping and aggregation service
"""
import feedparser
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings


class NewsScraperService:
    """Service for scraping news from various sources"""

    def __init__(self):
        self.headers = {
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.timeout = settings.REQUEST_TIMEOUT

    def scrape_rss_feed(self, feed_url: str, source_name: str, source_type: str) -> List[Dict]:
        """
        Scrape articles from an RSS feed
        """
        articles = []

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:20]:  # Limit to 20 most recent
                try:
                    # Parse published date
                    published_date = None
                    if hasattr(entry, 'published_parsed'):
                        published_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed'):
                        published_date = datetime(*entry.updated_parsed[:6])
                    else:
                        published_date = datetime.utcnow()

                    # Only get recent articles (last 7 days)
                    if published_date < datetime.utcnow() - timedelta(days=7):
                        continue

                    article = {
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'source': source_name,
                        'source_type': source_type,
                        'published_date': published_date,
                        'summary': entry.get('summary', ''),
                        'author': entry.get('author', ''),
                    }

                    # Try to get full content
                    full_content = self.extract_article_content(entry.get('link', ''))
                    if full_content:
                        article['content'] = full_content

                    articles.append(article)

                except Exception as e:
                    print(f"Error parsing feed entry: {e}")
                    continue

            print(f"Scraped {len(articles)} articles from {source_name}")

        except Exception as e:
            print(f"Error scraping RSS feed {feed_url}: {e}")

        return articles

    def extract_article_content(self, url: str) -> Optional[str]:
        """
        Extract full article content from URL using newspaper3k
        """
        try:
            article = Article(url)
            article.download()
            article.parse()

            return article.text

        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None

    def scrape_webpage(self, url: str, source_name: str, source_type: str) -> List[Dict]:
        """
        Scrape articles from a webpage (for non-RSS sources)
        """
        articles = []

        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Look for article links (this is a generic approach)
            # In production, you'd want custom scrapers for each source
            article_links = soup.find_all('a', href=True)

            for link in article_links[:20]:
                try:
                    article_url = link['href']

                    # Make URL absolute
                    if article_url.startswith('/'):
                        from urllib.parse import urljoin
                        article_url = urljoin(url, article_url)

                    # Skip if not a valid article URL
                    if not article_url.startswith('http'):
                        continue

                    # Extract article
                    article = Article(article_url)
                    article.download()
                    article.parse()

                    if len(article.text) < settings.MIN_CONTENT_LENGTH:
                        continue

                    articles.append({
                        'title': article.title or link.get_text().strip(),
                        'url': article_url,
                        'source': source_name,
                        'source_type': source_type,
                        'published_date': article.publish_date or datetime.utcnow(),
                        'content': article.text,
                        'author': ', '.join(article.authors) if article.authors else '',
                    })

                except Exception as e:
                    continue

            print(f"Scraped {len(articles)} articles from {source_name}")

        except Exception as e:
            print(f"Error scraping webpage {url}: {e}")

        return articles

    def scrape_all_sources(self) -> List[Dict]:
        """
        Scrape all configured news sources
        """
        all_articles = []

        for source_type, urls in settings.NEWS_SOURCES.items():
            for url in urls:
                try:
                    # Determine source name from URL
                    from urllib.parse import urlparse
                    source_name = urlparse(url).netloc.replace('www.', '')

                    # Try RSS feed first
                    articles = self.scrape_rss_feed(url, source_name, source_type)

                    # If RSS didn't work or returned no results, try webpage scraping
                    if not articles and not url.endswith(('.rss', '.xml')):
                        articles = self.scrape_webpage(url, source_name, source_type)

                    all_articles.extend(articles)

                    # Rate limiting
                    time.sleep(2)

                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                    continue

        return all_articles

    def search_google_news(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google News for specific topics (requires additional setup)
        This is a placeholder - in production you'd use Google News API or similar
        """
        # Placeholder for Google News integration
        # You could use: googlenews-python, pygooglenews, or newspaper3k with Google News
        return []

    def fetch_specific_sources(self, urls: List[str]) -> List[Dict]:
        """
        Fetch articles from specific URLs
        """
        articles = []

        for url in urls:
            try:
                content = self.extract_article_content(url)
                if content:
                    from urllib.parse import urlparse
                    source_name = urlparse(url).netloc.replace('www.', '')

                    # Try to parse with newspaper
                    article = Article(url)
                    article.download()
                    article.parse()

                    articles.append({
                        'title': article.title or 'Untitled',
                        'url': url,
                        'source': source_name,
                        'source_type': 'custom',
                        'published_date': article.publish_date or datetime.utcnow(),
                        'content': content,
                        'author': ', '.join(article.authors) if article.authors else '',
                    })

            except Exception as e:
                print(f"Error fetching {url}: {e}")

        return articles


class CustomSourceScrapers:
    """
    Custom scrapers for specific sources that need special handling
    """

    @staticmethod
    def scrape_mckinsey() -> List[Dict]:
        """Custom scraper for McKinsey articles"""
        # Implement custom logic for McKinsey's website structure
        pass

    @staticmethod
    def scrape_hbr() -> List[Dict]:
        """Custom scraper for Harvard Business Review"""
        # Implement custom logic for HBR's website structure
        pass

    @staticmethod
    def scrape_gartner() -> List[Dict]:
        """Custom scraper for Gartner research"""
        # Implement custom logic for Gartner's website structure
        pass


def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """
    Remove duplicate articles based on URL
    """
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)

    return unique_articles


def filter_articles(articles: List[Dict], min_length: int = None) -> List[Dict]:
    """
    Filter articles by quality criteria
    """
    min_length = min_length or settings.MIN_CONTENT_LENGTH
    filtered = []

    for article in articles:
        # Check minimum content length
        content = article.get('content', '')
        if len(content) < min_length:
            continue

        # Check for required fields
        if not article.get('title') or not article.get('url'):
            continue

        # Check language (if specified)
        # This is a simple check - in production you'd use proper language detection
        if settings.ALLOWED_LANGUAGES and 'en' in settings.ALLOWED_LANGUAGES:
            # Assume English for now, could add langdetect library
            pass

        filtered.append(article)

    return filtered


if __name__ == "__main__":
    # Test scraping
    scraper = NewsScraperService()
    articles = scraper.scrape_all_sources()
    articles = deduplicate_articles(articles)
    articles = filter_articles(articles)

    print(f"Total unique articles: {len(articles)}")
    for i, article in enumerate(articles[:5], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   URL: {article['url']}")
