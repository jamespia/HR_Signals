"""
AI-powered content analysis and summarization service
"""
import asyncio
from typing import Dict, List, Optional, Tuple
from anthropic import Anthropic
import json
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings


class AIAnalysisService:
    """Service for AI-powered content analysis using Claude"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        self.client = Anthropic(api_key=self.api_key)
        self.model = settings.AI_MODEL

    async def analyze_article(self, title: str, content: str, url: str) -> Dict:
        """
        Comprehensive article analysis including summarization, theme classification,
        key takeaways extraction, and sentiment analysis
        """
        prompt = f"""You are an expert HR and workforce analyst. Analyze the following article and provide a comprehensive analysis.

Article Title: {title}
Article URL: {url}
Content:
{content[:5000]}  # Limit content length

Please provide:
1. A concise executive summary (2-3 sentences, max 500 characters)
2. 3-5 key takeaways (actionable insights)
3. Primary theme classification (choose ONE that best fits):
   - Workforce Transformation
   - AI Governance
   - Skills and Capability
   - HR Technology
   - Policy and Regulation
   - Future of Work
   - Employee Experience
   - Talent Acquisition
   - Diversity and Inclusion
   - Organizational Culture
4. Secondary themes (choose up to 2 additional themes from the list above)
5. Geographic region (Global, Australia, Asia Pacific, North America, Europe, UK)
6. Industry sectors mentioned (up to 3): Technology, Financial Services, Healthcare, Manufacturing, Retail, Professional Services, Public Sector, Education, Energy, General
7. Sentiment (positive, negative, neutral) with explanation
8. Signal strength (0-1): How significant/impactful is this for HR leaders?
9. Time horizon: immediate, short-term (1-2 years), long-term (3+ years)
10. Is this an emerging trend not yet mainstream? (yes/no)

Provide your response in the following JSON format:
{{
  "summary": "Executive summary here...",
  "key_takeaways": ["takeaway 1", "takeaway 2", "takeaway 3"],
  "primary_theme": "Theme name",
  "secondary_themes": ["Theme 1", "Theme 2"],
  "confidence_score": 0.95,
  "region": "Region name",
  "sectors": ["Sector 1", "Sector 2"],
  "sentiment": "positive",
  "sentiment_explanation": "Brief explanation",
  "sentiment_score": 0.7,
  "signal_strength": 0.8,
  "time_horizon": "short-term",
  "is_emerging": false,
  "impact_level": "high"
}}

Provide only the JSON response, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            content = response.content[0].text

            # Try to extract JSON if wrapped in markdown
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            # Parse JSON
            analysis = json.loads(content)

            return analysis

        except Exception as e:
            print(f"Error in AI analysis: {e}")
            # Return default analysis if AI fails
            return self._default_analysis()

    async def extract_insights(self, articles: List[Dict]) -> List[Dict]:
        """
        Extract cross-cutting insights from multiple articles
        """
        if not articles:
            return []

        # Prepare article summaries
        article_text = "\n\n".join([
            f"Article {i+1}: {art['title']}\nSummary: {art.get('summary', 'N/A')}"
            for i, art in enumerate(articles[:10])  # Limit to 10 articles
        ])

        prompt = f"""You are an expert HR strategist. Based on the following articles, identify 5-7 cross-cutting insights that HR and transformation leaders should know.

Articles:
{article_text}

For each insight, provide:
1. A clear, actionable title
2. A brief description (2-3 sentences)
3. Impact level (high, medium, low)
4. Time horizon (immediate, short-term, long-term)
5. Relevance score (0-1)

Provide your response in JSON format:
{{
  "insights": [
    {{
      "title": "Insight title",
      "description": "Detailed description",
      "impact_level": "high",
      "time_horizon": "short-term",
      "relevance_score": 0.9
    }}
  ]
}}

Provide only the JSON response."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.4,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            # Extract JSON
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            result = json.loads(content)
            return result.get("insights", [])

        except Exception as e:
            print(f"Error extracting insights: {e}")
            return []

    async def detect_emerging_trends(self, articles: List[Dict], existing_trends: List[str]) -> List[Dict]:
        """
        Detect emerging trends from recent articles
        """
        if not articles:
            return []

        article_text = "\n\n".join([
            f"- {art['title']} ({art.get('primary_theme', 'N/A')})"
            for art in articles[:20]
        ])

        existing_trends_text = "\n".join([f"- {trend}" for trend in existing_trends])

        prompt = f"""You are a trend analyst specializing in HR and workforce topics. Based on recent articles, identify 3-5 EMERGING trends that are NOT yet mainstream or widely covered.

Recent Articles:
{article_text}

Existing Known Trends (do NOT repeat these):
{existing_trends_text}

For each emerging trend, provide:
1. Name (concise, descriptive)
2. Description (what is it and why it matters)
3. Keywords (5-7 related terms)
4. Status (emerging, growing)
5. Momentum score (0-1)

Provide your response in JSON format:
{{
  "trends": [
    {{
      "name": "Trend name",
      "description": "What this trend means...",
      "keywords": ["keyword1", "keyword2"],
      "status": "emerging",
      "momentum": 0.7
    }}
  ]
}}

Provide only the JSON response."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.5,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            result = json.loads(content)
            return result.get("trends", [])

        except Exception as e:
            print(f"Error detecting trends: {e}")
            return []

    async def generate_digest(
        self,
        articles: List[Dict],
        insights: List[Dict],
        trends: List[Dict],
        period: str = "daily"
    ) -> Dict:
        """
        Generate executive digest (daily or weekly)
        """
        articles_text = "\n\n".join([
            f"**{art['title']}**\nTheme: {art.get('primary_theme', 'N/A')}\nSummary: {art.get('summary', 'N/A')}"
            for art in articles[:15]
        ])

        insights_text = "\n".join([
            f"- {ins['title']}: {ins['description']}"
            for ins in insights[:5]
        ])

        trends_text = "\n".join([
            f"- {t['name']}: {t.get('description', 'Emerging trend')}"
            for t in trends[:5]
        ])

        prompt = f"""You are an executive communications expert. Create a {period} digest for HR and transformation leaders.

Top Articles:
{articles_text}

Key Insights:
{insights_text}

Emerging Trends:
{trends_text}

Create a compelling executive digest with:
1. A punchy title
2. A 2-paragraph executive summary highlighting the most important developments
3. Top 3 stories to watch
4. 2-3 strategic implications for HR leaders

Provide your response in JSON format:
{{
  "title": "Digest title",
  "summary": "Executive summary...",
  "top_stories": ["Story 1", "Story 2", "Story 3"],
  "strategic_implications": ["Implication 1", "Implication 2"]
}}

Provide only the JSON response."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.4,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            result = json.loads(content)
            return result

        except Exception as e:
            print(f"Error generating digest: {e}")
            return {
                "title": f"{period.capitalize()} HR Signals Digest",
                "summary": "Error generating digest",
                "top_stories": [],
                "strategic_implications": []
            }

    def _default_analysis(self) -> Dict:
        """Return default analysis when AI fails"""
        return {
            "summary": "Summary unavailable",
            "key_takeaways": [],
            "primary_theme": "General",
            "secondary_themes": [],
            "confidence_score": 0.0,
            "region": "Global",
            "sectors": ["General"],
            "sentiment": "neutral",
            "sentiment_explanation": "N/A",
            "sentiment_score": 0.0,
            "signal_strength": 0.5,
            "time_horizon": "short-term",
            "is_emerging": False,
            "impact_level": "medium"
        }


# Helper function for batch processing
async def batch_analyze_articles(articles: List[Dict], api_key: Optional[str] = None) -> List[Dict]:
    """
    Analyze multiple articles in batch with concurrency control
    """
    service = AIAnalysisService(api_key)

    # Process in batches to avoid rate limits
    batch_size = 5
    results = []

    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        tasks = [
            service.analyze_article(
                title=art.get('title', ''),
                content=art.get('content', ''),
                url=art.get('url', '')
            )
            for art in batch
        ]

        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        results.extend(batch_results)

        # Rate limiting delay
        if i + batch_size < len(articles):
            await asyncio.sleep(1)

    return results
