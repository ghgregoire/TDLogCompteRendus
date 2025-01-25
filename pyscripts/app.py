from flask import Flask, request, render_template, redirect, url_for, Markup, g
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

"""
@app.route('/')
def index():
    return render_template('index.html')
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.before_request
def before_request():
    # Exemple de variable dynamique (modifiable à chaque requête)
    g.dynamic_data = {"status": "processing"}


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Aucun fichier détecté", 400

    file = request.files['file']

    if file.filename == '':
        return "Nom de fichier vide", 400

    if file and allowed_file(file.filename):

        # Sauvegarde du fichier dans le dossier upload

        # Générer un nom standardisé pour le fichier
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"video_{timestamp}.mp4"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        g.dynamic_data['file_path'] = filepath

        # Rediriger ou notifier l'utilisateur
        print(f"Fichier résumé et enregistré sous : {resultat}", 200)
        return render_template("uploaded.html")
    else:
        return "Extension non autorisée", 400

if __name__ == '__main__':
    app.run(debug=True)
