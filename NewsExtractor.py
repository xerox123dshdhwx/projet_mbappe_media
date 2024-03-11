import os
import subprocess
import jsonlines
from Media import Media

class NewsExtractor:
    def __init__(self, media: Media):
        self.media = media
        # Utilisation de os.path.join pour une meilleure compatibilité entre les OS
        self.project_dir = os.path.abspath(os.path.join('spiders', 'media_scraping', 'media_scraping', 'spiders'))

    def extract_news_text(self):
        article_url = self.media.get_article_to_reduce_url()

        # Chemins absolus pour les fichiers de sortie
        # Utilisation de os.path.join pour construire le chemin de manière dynamique
        output_path = os.path.abspath(os.path.join('spiders', 'media_scraping', 'media_scraping', 'article_content.jsonl'))

        # Assure que le répertoire pour output_path existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Exécution du spider Scrapy
        try:
            subprocess.run([
                'scrapy', 'crawl', 'news_spider',
                '-a', f'article_url={article_url}',
                '-o', output_path
            ], cwd=self.project_dir, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de Scrapy: {e}")
            return ''

        # Traitement du fichier de sortie si Scrapy s'exécute avec succès
        try:
            with jsonlines.open(output_path) as reader:
                for obj in reader:
                    text = obj.get("text", "")
                    return ' '.join(text.split())
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier de sortie: {e}")
            return ''

        return ''
