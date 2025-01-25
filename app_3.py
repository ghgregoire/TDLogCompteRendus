from flask import Flask, request, render_template, redirect, url_for, Markup, g
import os
from datetime import datetime
import main
import openai
message_history=[]

###############################################
def compterendu_basededonnee():
    #with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    #    transcription = f.read()
        # Appel à l'API OpenAI pour générer le résumé
    message_history = []
    filename = os.path.join(os.path.dirname(__file__), "modele_basededonnee.txt")
    document = main.read_txt(filename)
    chunks = main.split_text(document)
    filename2 = os.path.join(os.path.dirname(__file__), "transcription.txt")
    document2 = main.read_txt(filename2)
    chunks2 = main.split_text(document2)
    message_history.append({"role": "user", "content": chunks[0]})
    message_history.append({"role": "user", "content": chunks2[0]})
    message_history.append({"role": "user",
                                "content": "génère un texte (avec des sauts de lignes markup et le titre en gras markup pour chaque élement ) permettant de produire un compte rendu sous forme de base de donnée  a partir de la trancription de reunion, en respectant le format imposé"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history, max_tokens=450
    )

    summary = response.choices[0].message['content']
    text_file_path = filename2.replace('.txt', '_resume.txt')
    with open(text_file_path, 'w') as text_file:
        text_file.write(summary)
    print(f"resume sauvegardée dans {text_file_path}")
    return summary   
###############################################
import re

def format_text_for_html(text):
    # Transformer les balises Markdown `**` en `<strong>`
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)  # Transforme les ** en <strong>
    
    # Gérer les listes Markdown en HTML `<ul>` et `<li>`
    text = re.sub(r'(?m)^- (.+)$', r'<li>\1</li>', text)  # Transforme les - items en <li>
    text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)  # Ajoute <ul> autour des <li>

    # Transformer les sauts de ligne en `<br>`
    text = text.replace('\n', '<br>')

    return text

app = Flask(__name__)
@app.route("/")
def home():
    result=compterendu_basededonnee()
    return render_template("upload.html", dynamic_message=format_text_for_html(Markup(result)))
    
if __name__ == '__main__':
    app.run(debug=True)