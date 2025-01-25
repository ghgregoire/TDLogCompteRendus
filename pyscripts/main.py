from flask import Flask
from flask import render_template,Markup
from flask import request



from flask import jsonify

########################charge la clé openai
import openai


from io import StringIO
import fitz
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

import os
import subprocess
import whisper

import openai

from app import app
"""
@app.route("/")
def home():
    return render_template("index.html", dynamic_message=Markup(compte_rendu))
"""

# !apt-get update && apt-get install ffmpeg -y
def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


# Clé de Adle
openai.api_key_path = ".venv/APIKEY.txt"

#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.organization = os.getenv("OPENAI_ORGANIZATION")

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

def transcribe_video(video_path, language="fr", model_name="medium"):




    audio_path = "sample-3.mp3"  # Define the audio path variable
    if os.path.exists(audio_path):
        os.remove(audio_path)
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
    with open("transcription.txt", "w", encoding="utf-8") as f:
       f.write(result["text"])

    # SAUVEGARDER DANS LA BASE DE DONNEE LA TRANSCRIPTION
    # SAUVEGARDER DANS LA BASE DE DONNEE LA TRANSCRIPTION
    # SAUVEGARDER DANS LA BASE DE DONNEE LA TRANSCRIPTION



print("1")
# transcribe_video("WIN_20241125_16_02_40_Pro.mp4")




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

def compterendu():
    #with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    #    transcription = f.read()
        # Appel à l'API OpenAI pour générer le résumé
    message_history = []
    filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
    document = read_pdf(filename)
    chunks = split_text(document)
    filename2 = os.path.join(os.path.dirname(__file__), "transcription.txt")
    document2 = read_txt(filename2)
    chunks2 = split_text(document2)
    message_history.append({"role": "user", "content": chunks[0]})
    message_history.append({"role": "user", "content": chunks2[0]})
    message_history.append({"role": "user",
                                "content": "le premir fichier est un modele de compte rendu de réunion. Le deuxième est supposé être une transcription de réunion (si ce n'est pas le cas, faites au mieux comme si c'en était une). Veuillez faire un compte rendu de la réunion en utilisant le modèle. Commencez votre message par un rédumé en une phrase courte."})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history, max_tokens=450
    )

    summary = response.choices[0].message['content']
    text_file_path = filename2.replace('.txt', '_resume.txt')
    with open(text_file_path, 'w') as text_file:
        text_file.write(summary)
    print(f"resume sauvegardée dans {text_file_path}")

    # SAUVEGARDER DANS LA BASE DE DONNEE LE RESUME CORRESPONDANT
    # SAUVEGARDER DANS LA BASE DE DONNEE LE RESUME CORRESPONDANT
    # SAUVEGARDER DANS LA BASE DE DONNEE LE RESUME CORRESPONDANT

    return summary


def traiter_video():
    video_dir = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    fichiers = os.listdir(video_dir)

    if fichiers:
        for fichier in fichiers:
            print(f"Traitement de la vidéo : {fichier}")
            # Ajouter votre logique de traitement ici
    else:
        print("Aucune vidéo à traiter")

def process(gdata):
    file_path = gdata.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return {"error": "File not found"}

    # Exemple : Obtenir la taille du fichier
    file_size = os.path.getsize(file_path)
    print("file")

    transcribe_video(file_path)
    print("video transcrite")


    return {
        "status": "completed",
        "file_size": file_size,
        "file_name": os.path.basename(file_path),
        "file_resume": compterendu()
    }

#compte_rendu = generer_compte_rendu(transcribe_video("WIN_20241125_16_02_40_Pro.mp4"))
#compte_rendu = process()
#compte_rendu = compterendu("WIN_20241125_16_02_40_Pro_transcription.txt")
# dialogue = " Je m'appelle Armand, je suis à l'école de Pont-et-Choussey, avec Grégoire, qui reste de moi. Je veux parler de l'extérieur qui va détruire l'interstructure."
# compte_rendu = generer_compte_rendu(dialogue)
#if compte_rendu:
#    print("\nCompte Rendu de la Réunion :\n")
#    print(compte_rendu)
