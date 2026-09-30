"""
Lector de noticias financieras para el pipeline de análisis financiero.
Se conecta a APIs de noticias (Bloomberg, Reuters, etc.) y extrae artículos relevantes.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional, Set
from dataclasses import dataclass, field
from urllib.parse import quote_plus

import pandas as pd
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class NewsArticle:
    """Representa un artículo de noticia financiera."""
    article_id: str
    headline: str
    summary: str
    content: str
    source: str
    url: str
    published_at: datetime
    authors: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None
    relevance_score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "article_id": self.article_id,
            "headline": self.headline,
            "summary": self.summary,
            "content": self.content,
            "source": self.source,
            "url": self.url,
            "published_at": self.published_at.isoformat(),
            "authors": self.authors,
            "tags": self.tags,
            "sentiment_score": self.sentiment_score,
            "relevance_score": self.relevance_score,
            "metadata": self.metadata
        }


class FinancialNewsReader:
    """
    Clase principal para leer noticias financieras de múltiples fuentes.
    Soporta APIs de noticias, RSS feeds y archivos procesados.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config.get("source_type", "api")
        self.source_credentials = config.get("credentials", {})
        self.batch_size = config.get("batch_size", 100)
        self.max_retries = config.get("max_retries", 3)
        self.keywords = config.get("keywords", [])
        self.categories = config.get("categories", [])
        self._s3_client = None
        self._api_session = None

    def _get_s3_client(self):
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self.source_credentials.get("aws_access_key"),
                aws_secret_access_key=self.source_credentials.get("aws_secret_key"),
                region_name=self.source_credentials.get("region", "us-east-1")
            )
        return self._s3_client

    def _retry_with_backoff(self, func, *args, **kwargs):
        import time
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                wait_time = 2 * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
        raise last_exception

    def _build_query_params(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Construye parámetros de query para la API de noticias."""
        params = {
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "language": "en",
            "sortby": "publishedAt",
            "pageSize": self.batch_size
        }

        if self.keywords:
            params["q"] = " OR ".join(self.keywords)

        if self.categories:
            params["categories"] = ",".join(self.categories)

        return params

    def read_from_api(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Lee noticias desde API de noticias financieras (NewsAPI, Bloomberg, etc.)
        """
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        api_url = self.source_credentials.get("api_url")
        api_key = self.source_credentials.get("api_key")

        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

        params = self._build_query_params(start_date, end_date)
        page = 1

        while True:
            params["page"] = page

            try:
                response = session.get(
                    f"{api_url}/articles",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                articles = data.get("articles", [])
                if not articles:
                    break

                for article_data in articles:
                    yield self._parse_article(article_data)

                if page >= data.get("totalPages", 1):
                    break

                page += 1

            except requests.RequestException as e:
                logger.error(f"News API request failed: {str(e)}")
                break

    def read_from_s3(
        self,
        bucket: str,
        prefix: str,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Lee noticias procesadas previamente desde S3.
        """
        s3_client = self._get_s3_client()

        date_format = "%Y-%m-%d"
        date_range = pd.date_range(start_date, end_date, freq='D')

        for date_obj in date_range:
            date_str = date_obj.strftime(date_format)
            object_key = f"{prefix}/date={date_str}/news.parquet"

            try:
                response = s3_client.get_object(Bucket=bucket, Key=object_key)
                data = response['Body'].read()

                df = pd.read_parquet(pd.io.common.BytesIO(data))

                for _, row in df.iterrows():
                    yield self._row_to_news_article(row)

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code == 'NoSuchKey':
                    logger.info(f"No news file for date {date_str}")
                    continue
                logger.error(f"S3 error reading {object_key}: {str(e)}")
                raise

    def read_from_rss(
        self,
        feed_urls: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Lee noticias desde RSS feeds de fuentes financieras.
        """
        import feedparser

        for feed_url in feed_urls:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries:
                    published = self._parse_rss_date(entry.get("published", ""))

                    if published < start_date or published > end_date:
                        continue

                    yield NewsArticle(
                        article_id=entry.get("id", entry.link),
                        headline=entry.get("title", ""),
                        summary=entry.get("summary", ""),
                        content=entry.get("content", [{}])[0].get("value", ""),
                        source=feed.feed.get("title", "Unknown"),
                        url=entry.link,
                        published_at=published,
                        authors=[author.get("name", "") for author in entry.get("authors", [])],
                        tags=[tag.get("term", "") for tag in entry.get("tags", [])],
                        metadata={"feed": feed_url}
                    )

            except Exception as e:
                logger.error(f"Error parsing RSS feed {feed_url}: {str(e)}")
                continue

    def _parse_rss_date(self, date_str: str) -> datetime:
        """Parsea fecha de RSS feed."""
        from email.utils import parsedate_to_datetime
        try:
            return parsedate_to_datetime(date_str)
        except Exception:
            try:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except Exception:
                return datetime.now()

    def _parse_article(self, data: Dict[str, Any]) -> NewsArticle:
        """Convierte respuesta de API a NewsArticle."""
        published_str = data.get("publishedAt", data.get("published_at", ""))
        try:
            published_at = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        except Exception:
            published_at = datetime.now()

        return NewsArticle(
            article_id=data.get("url", data.get("id", "")),
            headline=data.get("title", ""),
            summary=data.get("description", data.get("summary", "")),
            content=data.get("content", data.get("body", "")),
            source=data.get("source", {}).get("name", "Unknown"),
            url=data.get("url", ""),
            published_at=published_at,
            authors=data.get("author", "").split(", ") if data.get("author") else [],
            tags=data.get("keywords", "").split(", ") if data.get("keywords") else [],
            sentiment_score=data.get("sentiment_score"),
            relevance_score=data.get("relevance_score"),
            metadata=data.get("metadata", {})
        )

    def _row_to_news_article(self, row: pd.Series) -> NewsArticle:
        """Convierte fila de DataFrame a NewsArticle."""
        return NewsArticle(
            article_id=str(row['article_id']),
            headline=str(row['headline']),
            summary=str(row['summary']),
            content=str(row['content']),
            source=str(row['source']),
            url=str(row['url']),
            published_at=pd.to_datetime(row['published_at']),
            authors=list(row['authors']) if 'authors' in row else [],
            tags=list(row['tags']) if 'tags' in row else [],
            sentiment_score=float(row['sentiment_score']) if pd.notna(row.get('sentiment_score')) else None,
            relevance_score=float(row['relevance_score']) if pd.notna(row.get('relevance_score')) else None,
            metadata=dict(row['metadata']) if 'metadata' in row and pd.notna(row.get('metadata')) else {}
        )

    def read(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Método principal que delega según la configuración de fuente.
        """
        logger.info(
            f"Reading financial news from {start_date} to {end_date}"
        )

        if self.source_type == "api":
            yield from self.read_from_api(start_date, end_date)
        elif self.source_type == "s3":
            bucket = self.source_credentials.get("s3_bucket")
            prefix = self.source_credentials.get("s3_prefix", "news")
            yield from self.read_from_s3(bucket, prefix, start_date, end_date)
        elif self.source_type == "rss":
            feed_urls = self.source_credentials.get("rss_feeds", [])
            yield from self.read_from_rss(feed_urls, start_date, end_date)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def read_as_dataframe(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        Retorna los datos como DataFrame de pandas.
        """
        records = list(self.read(start_date, end_date))
        if not records:
            return pd.DataFrame()

        data = [record.to_dict() for record in records]
        df = pd.DataFrame(data)

        df['published_at'] = pd.to_datetime(df['published_at'])
        logger.info(f"Loaded {len(df)} news articles")

        return df

    def filter_by_keywords(
        self,
        articles: Iterator[NewsArticle],
        keywords: List[str]
    ) -> Iterator[NewsArticle]:
        """
        Filtra artículos por palabras clave en headline o contenido.
        """
        keywords_lower = [k.lower() for k in keywords]

        for article in articles:
            text = f"{article.headline} {article.summary} {article.content}".lower()
            if any(kw in text for kw in keywords_lower):
                yield article

    def close(self):
        """Cleanup de recursos."""
        logger.info("Financial news reader closed")


def create_reader(config_path: str = "conf/dev_config.json") -> FinancialNewsReader:
    """Factory para crear reader desde archivo de configuración."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return FinancialNewsReader(config.get("financial_news", {}))