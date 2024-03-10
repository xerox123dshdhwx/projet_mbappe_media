import json
import scrapy
from datetime import datetime
from urllib.parse import urlparse


class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['francetvinfo.fr', 'theguardian.com', 'euronews.com']

    def __init__(self, article_url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.article_url = article_url

    domain_cookies = {
        'theguardian.com': {'consentUUID': 'b7601197-7a95-4352-a61e-ffb8e5b958e5_27'},#TODO solution temporaire cookie pas available a l'infinie, trouve une autre solution
    }

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'FEEDS': {
            'article_content.jsonl': {
                'format': 'jsonlines',
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        domain = urlparse(self.article_url).netloc
        cookies = self.domain_cookies.get(domain, {})
        yield scrapy.Request(self.article_url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"Processing URL: {response.url}")
        if 'Set-Cookie' in response.headers:
            self.logger.debug(f"Received Cookies: {response.headers['Set-Cookie']}")
        else:
            self.logger.debug("No cookies received in response.")

        try:
            text = None
            if 'francetvinfo.fr' in response.url:
                content_div = 'c-body'
                text = response.css(f'div.{content_div} *::text').getall()
                text = ' '.join(text)
            elif 'theguardian.com' in response.url:
                content_div = 'article-body-commercial-selector'
                text = response.css(f'div.{content_div} *::text').getall()
                text = ' '.join(text)
            elif 'euronews.com' in response.url:
                json_ld = response.xpath('//script[@type="application/ld+json"]/text()').get()
                if json_ld:
                    data = json.loads(json_ld)
                    article = next((item for item in data["@graph"] if item["@type"] == "NewsArticle"), None)
                    if article and "articleBody" in article:
                        text = article["articleBody"]

            if text:
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield {
                    'date_scraped': current_date,
                    'text': text,
                    'url': response.url
                }
            else:
                self.logger.warning(f"No text found for URL: {response.url}")
        except Exception as e:
            self.logger.error(f"Error processing {response.url}: {e}")
