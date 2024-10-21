# TDLogCompteRendus
Projet de TDLOG de génrateur de Compte-Rendus de Réunion

Contacts :
• adle.ben-salem@eleves.enpc.fr
• edgar.duc@eleves.enpc.fr
• antony.feord@eleves.enpc.fr

1. Première Phase : Mise en Œuvre Initiale

• Génération de la Transcription
La première étape consiste à transcrire une courte vidéo de réunion (environ 2 à
3 minutes).
Outil suggéré : Whisper-v3*
L’objectif est également d’identifier les différents interlocuteurs afin de faciliter
l’analyse.

• Prétraitement de la Transcription
La transcription sera ensuite prétraitée en expérimentant diverses techniques de
segmentation ("chunking"). On commencera par un découpage fixe, puis un
découpage par interlocuteur ou par paragraphe.
Outil suggéré : Langchain/LLamaIndex

• Création du Prompt pour la Génération du Compte Rendu
Enfin, un prompt sera conçu pour générer un compte rendu synthétique à partir
des segments de texte prétraités.
Outil suggéré : GPT

2. Améliorations Possibles

• Mise à l'Échelle pour des Réunions Plus Longues
Étendre la solution pour gérer des réunions plus longues, pouvant aller jusqu’à
une heure.
• Amélioration par Recherche Vectorielle
Utiliser des techniques de recherche vectorielle pour améliorer la pertinence et
la qualité du compte rendu généré.
• Développement d'une Interface Utilisateur (Frontend)
Concevoir une interface utilisateur pour rendre l'outil plus accessible et
convivial.
• Statistiques
Concevoir un affichage de statistiques sur les temps de paroles/prises de paroles des différents interlocuteurs

Questions :

Format attendu ?
Licence pour les outils ?
