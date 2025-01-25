from flask import Flask, request, render_template, jsonify, Markup, g
import os
from datetime import datetime
import openai
import main
import re
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Création de l'application Flask
app = Flask(__name__)

# Configuration des répertoires et des tailles de fichiers
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Taille maximale des fichiers (50 Mo)


#############
message_history = []

# Extensions autorisées pour les fichiers
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Fonction pour vérifier les extensions de fichiers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route de la page d'accueil
@app.route("/")
def home():
    return render_template("index.html")

# Préparation des données avant chaque requête
@app.before_request
def before_request():
    g.dynamic_data = {"status": "processing"}

# Route pour télécharger des fichiers
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Aucun fichier détecté", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "Nom de fichier vide", 400
    
    if file and allowed_file(file.filename):
        # Générer un nom standardisé pour le fichier
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"video_{timestamp}.mp4"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        g.dynamic_data['file_path'] = filepath

        # Appel à la fonction de traitement du fichier
        resultat = main.process(g.dynamic_data)
        
        return render_template("upload.html", dynamic_message=Markup(resultat["file_resume"]))
    else:
        return "Extension non autorisée", 400

# Fonction pour effectuer la complétion GPT-3.5
filename = os.path.join(os.path.dirname(__file__), "transcription.txt")
document = main.read_txt(filename)
chunks = main.split_text(document)  
message_history = []
def gpt3_completion(prompt_user, model="gpt-3.5-turbo", max_tokens=450):
    global message_history
    message_history.append({"role": "user", "content": prompt_user})
    response = openai.ChatCompletion.create(
        model=model, messages=message_history, max_tokens=max_tokens
    )
    model_response = response.choices[0].message["content"].strip()
    message_history.append({"role": "assistant", "content": model_response})
    return model_response

# Route pour afficher la page de conversation
@app.route("/conversation", methods=["GET", "POST"])
def conversation():
    message_history.append({"role": "user", "content": chunks[0]})
    return render_template("index_conversation.html")

# Route pour envoyer un prompt et recevoir une réponse
@app.route("/prompt", methods=["POST", "GET"])
def prompt():
    if request.method == "POST":
        prompt = request.form["prompt"]
        ans = gpt3_completion(prompt)
        return jsonify({"answer": ans})

# Route pour poser une question prédéfinie
@app.route("/question", methods=["GET"])
def question():
    ans = gpt3_completion("tu es un assistant gpt qui réponds aux questions sur les réunions, présentes toi très rapidement et propose ton aide")
    return jsonify({"answer": ans})

# Route pour générer une réponse basée sur un prompt
@app.route("/answer", methods=["POST", "GET"])
def answer():
    prompt = request.form["prompt"]
    prompt = f"{prompt}\nRéponds à la requête de l'utilisateur"
    ans = gpt3_completion(prompt)
    return jsonify({"answer": ans})

# Fonction pour générer un compte rendu animé
def compterendu_anime():
    model_path = os.path.join(os.path.dirname(__file__), "modele_animation_js.txt")
    transcription_path = os.path.join(os.path.dirname(__file__), "transcription.txt")
    
    # Lecture des fichiers
    model_text = main.read_txt(model_path)
    transcription_text = main.read_txt(transcription_path)
    
    # Découper le texte en morceaux
    model_chunks = main.split_text(model_text)
    transcription_chunks = main.split_text(transcription_text)

    # Ajouter les morceaux dans l'historique des messages
    message_history.append({"role": "user", "content": model_chunks[0]})
    message_history.append({"role": "user", "content": transcription_chunks[0]})
    message_history.append({"role": "user", "content": "Génère un scénario animé en format Javascript, où chaque bot (bot1, bot2, etc.) représente un intervenant en respectant le modele que je t'ai donné"})

    # Appel à l'API OpenAI pour générer le scénario
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history, max_tokens=1500
    )
    scenario = response.choices[0].message["content"]

    # Sauvegarder le scénario dans un fichier JS
    js_folder = os.path.join(os.getcwd(), "static", "js")
    output_js_path = os.path.join(js_folder, "prompt_anime.js")
    with open(output_js_path, "w", encoding="utf-8") as js_file:
        js_file.write(scenario)
        js_file.write('''
function displayScenario(scenario) {
    const chatContainer = document.getElementById('chat-container');
    scenario.forEach((entry, index) => {
        setTimeout(() => {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('chat-message');
            const avatarImg = document.createElement('img');
            avatarImg.src = entry.avatar;
            avatarImg.alt = `${entry.bot} avatar`;
            avatarImg.classList.add('chat-avatar');
            const textDiv = document.createElement('div');
            textDiv.classList.add('chat-text');
            textDiv.innerHTML = `<strong>${entry.bot}:</strong> ${entry.message}`;
            messageDiv.appendChild(avatarImg);
            messageDiv.appendChild(textDiv);
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, index * 3000); // Affiche chaque message avec un délai de 3 secondes
    });
}
window.onload = () => { displayScenario(meetingScenario); };
''')
    print(f"Scénario animé sauvegardé dans {output_js_path}")

@app.route('/animation', methods=['GET', 'POST'])
def animation():
    if request.method == 'POST':
        # Traitement de la vidéo uploadée pour l'animation
        # Ajoutez ici le code pour traiter l'upload
          return render_template('index_anime.html')
    return render_template('index_anime.html')


# Fonction pour générer un compte rendu basé sur une base de données
def compterendu_basededonnee():
    model_path = os.path.join(os.path.dirname(__file__), "modele_basededonnee.txt")
    transcription_path = os.path.join(os.path.dirname(__file__), "transcription.txt")
    
    # Lecture des fichiers
    model_text = main.read_txt(model_path)
    transcription_text = main.read_txt(transcription_path)

    # Découper le texte en morceaux
    model_chunks = main.split_text(model_text)
    transcription_chunks = main.split_text(transcription_text)

    # Ajouter les morceaux dans l'historique des messages
    message_history.append({"role": "user", "content": model_chunks[0]})
    message_history.append({"role": "user", "content": transcription_chunks[0]})
    message_history.append({"role": "user", "content": "Génère un texte formaté en base de données à partir de la transcription de réunion, avec des titres en gras et des sauts de ligne."})

    # Appel à l'API OpenAI pour générer le résumé
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history, max_tokens=450
    )

    summary = response.choices[0].message['content']
    
    # Sauvegarde du résumé dans un fichier
    text_file_path = transcription_path.replace('.txt', '_resume.txt')
    with open(text_file_path, 'w') as text_file:
        text_file.write(summary)
    print(f"Résumé sauvegardé dans {text_file_path}")

    return summary

# Fonction pour formater le texte pour l'affichage HTML
def format_text_for_html(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)  # ** en <strong>
    text = re.sub(r'(?m)^- (.+)$', r'<li>\1</li>', text)  # - en <li>
    text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)  # <ul> autour des <li>
    text = text.replace('\n', '<br>')  # Sauts de ligne en <br>
    return text

# Route pour afficher le résumé en base de données
@app.route('/basededonnee', methods=['GET', 'POST'])
def basededonnee():
    if request.method == 'POST':
        # Traitement de la vidéo uploadée pour la base de données
        # Ajoutez ici le code pour traiter l'upload
        result=compterendu_basededonnee()
        return render_template("upload.html", dynamic_message=format_text_for_html(Markup(result)))

# Exécution de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
