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
import os
import subprocess
import whisper

!apt-get update && apt-get install ffmpeg -y

def transcribe_video(video_path, language="fr", model_name="medium"):
    # Extraire l'audio de la vidéo
    # Use f-string to correctly substitute the video_path variable
    audio_path = "/content/sample-3.mp3" # Define the audio path variable
    !ffmpeg -i {video_path} -vn {audio_path} # Use audio_path in the command

    # Charger le modèle Whisper
    model = whisper.load_model(model_name)

    # Transcrire l'audio
    # Use the audio_path variable when transcribing
    result = model.transcribe(audio_path, language=language)
    print("Transcription terminée!")

    # Sauvegarder la transcription dans un fichier texte
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])

transcribe_video("WIN_20241125_16_02_40_Pro.mp4")

