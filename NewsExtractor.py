import os
import subprocess
import jsonlines
from Media import Media

class NewsExtractor:
    def __init__(self, media: Media):
        self.media = media
        self.project_dir = os.path.abspath(os.path.join('spiders', 'media_scraping', 'media_scraping', 'spiders'))

    def extract_news_text(self):
        article_url = self.media.get_article_to_reduce_url()
        output_path = os.path.abspath(os.path.join('spiders', 'media_scraping', 'media_scraping', 'article_content.jsonl'))

        # Assure that the directory for output_path exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Attempt to create or open the file to ensure it exists
        try:
            with open(output_path, 'a') as f:
                pass  # Just open and close to ensure the file exists
        except Exception as e:
            print(f"Error ensuring output file exists: {e}")
            return ''

        # Execution of the Scrapy spider
        try:
            subprocess.run([
                'scrapy', 'crawl', 'news_spider',
                '-a', f'article_url={article_url}',
                '-o', output_path
            ], cwd=self.project_dir, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing Scrapy: {e}")
            return ''

        # Process the output file if Scrapy executes successfully
        try:
            with jsonlines.open(output_path) as reader:
                for obj in reader:
                    text = obj.get("text", "")
                    return ' '.join(text.split())
        except Exception as e:
            print(f"Error reading output file: {e}")
            return ''

        return '' #TODO add real gestion of error not just return nothing, do somehting to stop the code and go back to the main page
