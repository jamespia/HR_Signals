import feedparser
from pathlib import Path
from typing import List, Dict


def load_alert_queries(file_path: str) -> List[str]:
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def build_alert_feed_url(query: str) -> str:
    # Build a Google News RSS feed URL from the query.
    # This is a placeholder; for actual Google Alerts, use the alert-specific feed URL.
    encoded_query = query.replace(' ', '+')
    return f"https://news.google.com/rss/search?q={encoded_query}"


def fetch_google_alerts(query: str) -> List[Dict]:
    """
    Fetch articles for a given query from Google News RSS.
    Replace this logic with Google Alerts feed parsing if available.
    """
    url = build_alert_feed_url(query)
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")
        })
    return articles


def main():
    file_path = Path(__file__).resolve().parents[1] / 'alert_queries.txt'
    queries = load_alert_queries(file_path)
    for query in queries:
        articles = fetch_google_alerts(query)
        print(f"Fetched {len(articles)} articles for query: {query}")


if __name__ == '__main__':
    main()
