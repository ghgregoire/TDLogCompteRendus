from flask import Flask
from flask import render_template
from flask import request
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')
@app.route("/prompt", methods = ['POST'])
def prompt():
    if request.method == 'POST':
        msg = request.form['prompt']
        return {"answer":msg}
#fonction transcription (d'après gpt). La transcription se trouvera dans un fichier transcription.txt
import os
import subprocess
import whisper

def transcribe_video(video_path, language="fr", model_name="medium"):
    # Extraire l'audio de la vidéo
    audio_path = "audio_output.wav"
    ffmpeg_command = f"ffmpeg -i \"{video_path}\" -q:a 0 -map a {audio_path} -y"
    subprocess.run(ffmpeg_command, shell=True, check=True)
    
    # Charger le modèle Whisper
    model = whisper.load_model(model_name)
    
    # Transcrire l'audio
    result = model.transcribe(audio_path, language=language)
    print("Transcription terminée!")
    
    # Sauvegarder la transcription dans un fichier texte
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    # Nettoyer les fichiers intermédiaires
    os.remove(audio_path)

# Exemple d'utilisation
video_file = "input_video.mp4"
transcribe_video(video_file)
#####################################################


