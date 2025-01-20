import pandas as pd
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

code_right_answer=11*[0]

#Insertion of SQL ALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique
    name = db.Column(db.String(100), nullable=False)  # Nom de l'utilisateur
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email unique
    password = db.Column(db.String(100), nullable=False)  # Mot de passe
    videos = db.relationship('Video', backref='owner', lazy=True)  # Relation avec la table Video
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique
    video_url = db.Column(db.String(255), nullable=False)  # Lien de la vidéo
    video_length = db.Column(db.Integer, nullable=False)  # Longueur de la vidéo en secondes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers User

    def __init__(self, video_url, video_length, user_id):
        self.video_url = video_url
        self.video_length = video_length
        self.user_id = user_id

with app.app_context(): #creation of the tables
    db.create_all()

