from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Pour utiliser flash messages
db = SQLAlchemy(app)

# Modèle pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    videos = db.relationship('Video', backref='owner', lazy=True)  # Relation avec la table Video

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(255), nullable=False)
    video_length = db.Column(db.Integer, nullable=False)  # Longueur de la vidéo en secondes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers User

    def __init__(self, video_url, video_length, user_id):
        self.video_url = video_url
        self.video_length = video_length
        self.user_id = user_id

# Créer les tables dans la base de données
with app.app_context():
    db.create_all()

# Route pour afficher la page de connexion
@app.route('/')
def home():
    return render_template('PAGE HTML.html')

# Route pour traiter les informations du formulaire de connexion
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Vérifier si l'email existe déjà dans la base de données
    if User.query.filter_by(email=email).first():
        flash('Cet email est déjà utilisé. Veuillez en utiliser un autre.', 'danger')
        return redirect(url_for('PAGE DE LOG IN.html'))

    # Hachage du mot de passe avant de l'insérer dans la base de données
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Créer un nouvel utilisateur
    new_user = User(name=name, email=email, password=hashed_password)

    # Ajouter l'utilisateur à la base de données
    db.session.add(new_user)
    db.session.commit()

    flash('Compte créé avec succès !', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add_video', methods=['POST'])
def add_video():
    email = request.form['email']  # Email de l'utilisateur pour identifier le propriétaire
    video_url = request.form['video_url']
    video_length = int(request.form['video_length'])  # Longueur de la vidéo (en secondes)

    # Trouver l'utilisateur correspondant à l'email
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Utilisateur non trouvé. Veuillez vérifier l\'email.', 'danger')
        return redirect(url_for('home'))

    # Ajouter la vidéo dans la base de données
    new_video = Video(video_url=video_url, video_length=video_length, user_id=user.id)
    db.session.add(new_video)
    db.session.commit()

    flash('Vidéo ajoutée avec succès !', 'success')
    return redirect(url_for('home'))

@app.route('/videos/<email>')
def get_videos(email):
    # Trouver l'utilisateur via l'email
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Utilisateur non trouvé.', 'danger')
        return redirect(url_for('home'))

    # Récupérer les vidéos associées
    videos = Video.query.filter_by(user_id=user.id).all()

    # Afficher les vidéos dans la page
    return render_template('videos.html', videos=videos, user=user)

