from flask import Flask
from flask import render_template
from flask import request
from openai import OpenAI

app = Flask(__name__)

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


###########fonction transcription
#!pip install git+https://github.com/openai/whisper.git
#!pip install ffmpeg-python
import os
import subprocess
import whisper
import ffmpeg

#!apt-get update && apt-get install ffmpeg -y

def transcribe_video(video_path, language="fr", model_name="medium"):
    # Extraire l'audio de la vidéo
    # Use f-string to correctly substitute the video_path variable
    audio_path = "sample-3.mp3" # Define the audio path variable
    ffmpeg.input(video_path)
    ffmpeg.output(audio_path)
    ffmpeg.run()

    # Charger le modèle Whisper
    model = whisper.load_model(model_name)

    # Transcrire l'audio
    # Use the audio_path variable when transcribing
    result = model.transcribe(audio_path, language=language)
    print("Transcription terminée!")

    # Sauvegarder la transcription dans un fichier texte
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])

#copier collé de gemini, pour nous inspirer
def compterendu(filename, api_key):
    """
    Cette fonction prend un nom de fichier en entrée (ex: transcription.txt)
    et utilise l'API OpenAI pour créer un résumé de la réunion décrite dans le fichier.
    """
    openai.api_key = api_key 

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

transcribe_video("WIN_20241125_16_02_40_Pro.mp4")

