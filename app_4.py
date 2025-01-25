from flask import Flask, render_template, request, jsonify
from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
import main

load_dotenv()

filename = os.path.join(os.path.dirname(__file__), "transcription.txt")
document = main.read_txt(filename)
chunks = main.split_text(document)

message_history = []
message_history.append({"role": "user", "content": chunks[0]})


def gpt3_completion(prompt_user, model="gpt-3.5-turbo", max_tokens=450):
    global message_history

    message_history.append({"role": "user", "content": prompt_user})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history, max_tokens=450
    )
    model_response = response.choices[0].message["content"].strip()

    message_history.append({"role": "assistant", "content": model_response})

    return model_response

app = Flask(__name__)



@app.route("/")
def hello():
    return render_template("index_conversation.html")


@app.route("/prompt", methods=["POST", "GET"])
def prompt():
    if request.method == "POST":
        prompt = request.form["prompt"]
        ans = gpt3_completion(prompt)
        s = jsonify({"answer": ans})
        return s


@app.route("/question", methods=["GET"])
def question():
    ans = gpt3_completion("tu es un assitant gpt qui réponds aux quetions sur les réunions, présentes toi très rapidement et propose ton aide")
    s = jsonify({"answer": ans})
    return s


@app.route("/answer", methods=["POST", "GET"])
def answer():
    prompt = request.form["prompt"]
    prompt = (
        prompt
        + "\n"
        + "Réponds à la requête de l'utilisateur"
    )
    ans = gpt3_completion(prompt)
    s = jsonify({"answer": ans})
    return s


if __name__ == '__main__':
    app.run(debug=True, port=5000)