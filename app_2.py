from flask import Flask, request, render_template, redirect, url_for, Markup, g
import os
from datetime import datetime
import main
import openai

#####################
message_history=[]

def compterendu_anime():  #utiliser index_anime
    model = os.path.join(os.path.dirname(__file__), "modele_animation_js.txt")
    document = main.read_txt(model)
    chunks = main.split_text(document)
    filename2 = os.path.join(os.path.dirname(__file__), "transcription.txt")
    document2 = main.read_txt(filename2)
    chunks2 = main.split_text(document2)
    message_history.append({"role": "user", "content": chunks[0]})
    message_history.append({"role": "user", "content": chunks2[0]})
    message_history.append({"role": "user",
                                "content": "Génère un scénario animé en format Javascript, où chaque bot (bot1, bot2, etc.) représente un intervenant en respectant le modele que je t'ai donné"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history, max_tokens=1500
    )
    scenario = response.choices[0].message["content"]

    print("Sauvegarde du scénario...")
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

// Appeler la fonction pour lancer le scénario
window.onload = () => {
    displayScenario(meetingScenario);
};''')
    print(f"Scénario sauvegardé dans {output_js_path}")

###############################################
compterendu_anime()
#################################
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index_anime.html")
    
if __name__ == '__main__':
    app.run(debug=True)