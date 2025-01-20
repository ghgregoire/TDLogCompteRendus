from flask import Flask
from flask import render_template
from flask import request

# from openai import OpenAI

app = Flask(__name__)
"""
@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/prompt", methods = ['POST'])
def prompt():
    if request.method == 'POST':
        msg = request.form['prompt']
        return {"answer":msg}

"""
###########fonction transcription
# !pip install git+https://github.com/openai/whisper.git
# !pip install ffmpeg-python
import os
from dotenv import load_dotenv
import subprocess
import whisper
import ffmpeg
print(ffmpegy)

# !apt-get update && apt-get install ffmpeg -y

def transcribe_video(video_path, language="fr", model_name="medium"):
    # Extraire l'audio de la vidéo
    # Use f-string to correctly substitute the video_path variable

    audio_path = "sample-3.mp3"  # Define the audio path variable

    command = [
        'ffmpeg',
        '-i', video_path,  # Fichier vidéo d'entrée
        '-q:a', '0',  # Qualité audio
        '-map', 'a',  # Extraire uniquement la piste audio
        audio_path  # Fichier audio de sortie
    ]
    # Exécuter la commande
    subprocess.run(command, check=True)
    # Charger le modèle Whisper
    model = whisper.load_model(model_name)

    # Transcrire l'audio
    # Use the audio_path variable when transcribing
    result = model.transcribe(audio_path, language=language)
    print("Transcription terminée!")

    # Sauvegarder la transcription dans un fichier texte
    # with open("transcription.txt", "w", encoding="utf-8") as f:
    #    f.write(result["text"])

    return result["text"]


# copier collé de gemini, pour nous inspirer
"""
def compterendu(filename, api_key):
    
    openai.api_key = api_key #a remplacer par OPENAI_API_KEY, une fois le fichier .env créé

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            transcription = f.read()

        # Appel à l'API OpenAI pour générer le résumé
        response = openai.Completion.create(
            engine="text-davinci-003",  # Vous pouvez choisir un autre moteur si besoin
            prompt=f"Veuillez résumer la transcription suivante d'une réunion:\n\n{transcription}",
            max_tokens=150,  # Ajustez la longueur du résumé selon vos besoins
            n=1,
            stop=None,
            temperature=0.7, # Ajustez la température pour un résumé plus ou moins créatif
        )

        summary = response.choices[0].text.strip()
        return summary

    except FileNotFoundError:
        return f"Erreur: Fichier '{filename}' introuvable."
    except openai.error.OpenAIError as e:
        return f"Erreur OpenAI: {e}"


# Example usage 
api_key = "YOUR_API_KEY" # Remplacez par votre clé API OpenAI
summary = compterendu("transcription.txt", api_key)
print(summary)
"""

print("1")
# transcribe_video("WIN_20241125_16_02_40_Pro.mp4")

import openai

# Clé de Adle
openai.api_key_path = ".venv/APIKEY.txt"


def generer_compte_rendu(dialogue, length=1):
    """
    Prend un texte de dialogue (réunion) et retourne un compte rendu généré par GPT.
    """
    try:
        messages = [
            {"role": "system",
             "content": "Vous êtes un assistant chargé de rédiger des comptes rendus professionnels à partir des dialogues de réunions."},
            {"role": "user",
             "content": f"Voici le texte d'un dialogue de réunion :\n\n{dialogue}\n\nVeuillez rédiger un compte rendu professionnel et structuré de cette réunion."}
        ]

        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou "gpt-4" mais je crois pas qu'on l'ait
            messages=messages,
            max_tokens=length * len(dialogue),  # Nombres maximum de mots de la réponse, à ajuster.
            temperature=0.5
        )

        # Extraction du texte généré
        compte_rendu = response['choices'][0]['message']['content'].strip()
        return compte_rendu

    except Exception as e:
        print("Une erreur s'est produite :", e)
        return None


compte_rendu = generer_compte_rendu(transcribe_video("WIN_20241125_16_02_40_Pro.mp4"))
# dialogue = " Je m'appelle Armand, je suis à l'école de Pont-et-Choussey, avec Grégoire, qui reste de moi. Je veux parler de l'extérieur qui va détruire l'interstructure."
# compte_rendu = generer_compte_rendu(dialogue)
if compte_rendu:
    print("\nCompte Rendu de la Réunion :\n")
    print(compte_rendu)
    