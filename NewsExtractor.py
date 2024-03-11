import os
import subprocess
import jsonlines
from Media import Media


class NewsExtractor:
    def __init__(self, media: Media):
        self.media = media
        self.project_dir = os.path.abspath('spiders/media_scraping/media_scraping/spiders')

    def extract_news_text(self):
        article_url = self.media.get_article_to_reduce_url()

        # Chemins absolus pour les fichiers de sortie
        output_path = os.path.join(self.project_dir, 'article_content.jsonl')

        # Exécution du spider Scrapy
        process = subprocess.run([
            'scrapy', 'crawl', 'news_spider',
            '-a', f'article_url={article_url}',
            '-o', output_path
        ], cwd=self.project_dir, shell=True)

        # Vérifier le code de retour du subprocess
        if process.returncode == 0:
            # TODO: Refactor the existing code to improve its quality. Decide on how to store cleaned articles and maintain a historical record. Optimize the algorithm as well.
            try:
                with jsonlines.open(output_path) as reader:
                    for line in reader:
                        pass
                    res = line["text"]
                    print("res:", res)
                    return ' '.join(res.split())
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Erreur lors de l'exécution de Scrapy")
            return ''
