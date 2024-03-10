import re
import openai
import requests
from openai import OpenAI

from Media import Media
from NewsExtractor import NewsExtractor


def prompt_image(content: str):
    print(f"Generating image with content: {content}")

    # Assurez-vous que le prompt ne dépasse pas la limite de caractères.
    prompt = f"Create an image inspired by the following theme, avoiding any direct representation of specific personalities or public figures mentioned: {content} with dense atmosphere and details."[
             :1000]

    try:
        # Utilisation de la méthode 'generate' de l'API DALL·E 3
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        download_image(image_url, 'static/generated_image.jpg')
        print("Image generated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_image(image_url: str, path: str):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")


def process_response(response):
    print(f"Processing response: {response}")

    result = response.choices[0].message.content
    split_result = result.split("@@@")
    result_summary = split_result[0].strip()
    result_for_dalee = split_result[1].strip()

    # Split result using numbers at the start of a line followed by a dot as delimiters
    points = re.split(r'(?m)^\d+\.', result_summary)
    points = [point.strip() for point in points if
              point.strip()]  # Remove any empty strings or just spaces #TODO maybe useles need to double check

    return result_summary, result_for_dalee, points


def write_article(article_content: str):
    with open('static/Article.txt', "w", encoding="utf-8") as article_file:
        article_file.write(article_content)
        article_file.flush()
    print("article writted")


def generate_media_resumer_prompt(media: Media):
    print(f"Generating media resumer prompt for med ia: {media}")
    article_content = NewsExtractor(media).extract_news_text()

    return f"""À partir de l'article suivant : {article_content}, 
    1. Résumez-le en 5 points basés strictement sur les faits, sans interprétation ni supposition.
    2. Adaptez ces 5 points pour DALL·E en excluant spécifiquement tout contenu qui pourrait être jugé comme sensible, offensant, discriminatoire, ou qui mentionne des noms de politiciens, figures publiques, ou toute autre identité. Assurez-vous que l'adaptation est neutre et conforme aux normes de sécurité d'OpenAI.
    3. Le total des 5 points pour DALL·E ne doit pas dépasser 1000 caractères.
    4. Séparez les réponses par "@@@".
    """
