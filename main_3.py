from flask import Flask, render_template, request, jsonify
from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()

# Clé de Adle
openai.api_key_path = ".venv/APIKEY.txt"


message_history = []


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context

def read_txt(filename):

    """
    Lit le contenu d'un fichier texte et le retourne sous forme de chaîne de caractères.
    """
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier texte {filename}: {e}")



def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "transcription.txt")
document = read_txt(filename)
chunks = split_text(document)

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


@app.route("/perro", methods=["POST", "GET"])
def perro():
    ans = gpt3_completion(
        "Tu es un assistant gpt. Présente toi rapidement et propose ton aide, pour parler de la reunion"
    )
    s = jsonify({"answer": ans})
    return s


@app.route("/perro2", methods=["POST", "GET"])
def perro2():
    prompt = request.form["prompt"]
    prompt = prompt + "\n" + "Réponds rapidement et relances la conversation"
    ans = gpt3_completion(prompt)
    s = jsonify({"answer": ans})
    return s

