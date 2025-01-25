from flask import Flask, request, render_template, redirect, url_for, Markup, g, jsonify
import os
from datetime import datetime
import main

app = Flask(__name__)

# Répertoire pour sauvegarder les fichiers
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Taille maximale du fichier (50 Mo)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # En octets

# Extensions autorisées
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_text(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() == 'txt'

"""
@app.route('/')
def index():
    return render_template('index.html')
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/feedback_gpt")
def feedback_gpt():
    return render_template("feedback_gpt.html")

@app.route("/feedback_bot")
def feedback_bot():
    return render_template("feedback_bot.html")

@app.route("/feedback_txt")
def feedback_txt():
    return render_template("feedback_txt.html")

@app.before_request
def before_request():
    # Exemple de variable dynamique (modifiable à chaque requête)
    g.dynamic_data = {"status": "processing"}


@app.route('/uploaded', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Aucun fichier détecté", 400

    file = request.files['file']
    print(file)
    if file.filename == '':
        return "Nom de fichier vide", 400

    if file and allowed_file(file.filename):

        # Sauvegarde du fichier dans le dossier upload

        # Générer un nom standardisé pour le fichier
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"texte_{timestamp}.mp4"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        g.dynamic_data['file_path'] = filepath
        resultat = main.process(g.dynamic_data)

        print(f"Fichier résumé et enregistré sous : {resultat}", 200)
        return render_template("uploaded.html", dynamic_message=Markup(resultat["file_resume"]))

    if file and allowed_text(file.filename):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"video_{timestamp}.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("ok : "+filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            contenu = f.read()
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(contenu)
        print("ok write")

        g.dynamic_data['file_path'] = filepath
        resultat = main.textprocess(g.dynamic_data)
        print(f"Fichier résumé et enregistré sous : {resultat}", 200)
        return render_template("uploaded.html", dynamic_message=Markup(resultat["file_resume"]))
    else:
        return "Extension non autorisée", 400

@app.route("/")
def hello():
    return render_template("index_conversation.html")


@app.route("/prompt", methods=["POST", "GET"])
def prompt():
    if request.method == "POST":
        prompt = request.form["prompt"]
        ans = main.gpt3_completion(prompt)
        s = jsonify({"answer": ans})
        return s


@app.route("/perro", methods=["POST", "GET"])
def perro():
    ans = main.gpt3_completion(
        "Tu es un assistant gpt. Présente toi rapidement et propose ton aide, pour parler de la reunion"
    )
    s = jsonify({"answer": ans})
    return s


@app.route("/perro2", methods=["POST", "GET"])
def perro2():
    prompt = request.form["prompt"]
    prompt = prompt + "\n" + "Réponds rapidement et relances la conversation"
    ans = main.gpt3_completion(prompt)
    s = jsonify({"answer": ans})
    return s

if __name__ == '__main__':
    app.run(debug=True)
