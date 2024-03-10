import os
from flask import Flask, render_template, request
import openai

from utils import process_response, prompt_image, generate_media_resumer_prompt
from Media import Media

app = Flask(__name__)

# Configurer la clé API pour OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("POST request received")
        my_article = Media(request.form["article_url"])

        prompt_text = generate_media_resumer_prompt(my_article)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0,
        )

        result_summary, result_for_dallee, points = process_response(response)
        prompt_image(result_for_dallee)
        print('point :', points)
        print("Sending response to template")
        return render_template("index.html", result=result_summary, points=points)

    print("GET request, rendering template")
    return render_template("index.html", result=None)
