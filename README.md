## # FakeNews

# Description

Cette application Django permet de collecter les informations des utilisateurs et d'enregistrer leurs réponses à des questions. Elle inclut une fonctionnalité permettant d'exporter les réponses de chaque utilisateur dans un fichier CSV.


# Fonctionnalités

Collecte des informations des utilisateurs (âge, genre, niveau scolaire, ethnie).

Enregistrement des réponses des utilisateurs à des questions.

Exportation des réponses au format CSV dans un dossier spécifique.


# Prérequis

Avant d'installer l'application, assurez-vous d'avoir :

Python 3.x installé

Django installé (pip install django)

Pandas installé (pip install pandas)


# Installation

 - Clonez ce dépôt :

git clone https://github.com/votre-repo.git
cd votre-repo

- Installez les dépendances :

    pip install -r requirements.txt
Créer un environnement virtuel (nommé env) et l'activer :

   python -m venv env
   env\Scripts\activate


    changez le chemin du fichier contenant les question  dans view.py et l'adopter a votre emplacement   
     - df = pd.read_excel('C:/Users/Khalil/Desktop/MONAPP/Dataset_francais_mai2024.xlsx')


- Appliquez les migrations de la base de données :

    python manage.py makemigrations
    python manage.py migrate

- Démarrez le serveur Django :

    python manage.py runserver

# Utilisation

- Ajouter un utilisateur

Accédez à http://localhost:8000/user_info/ pour entrer les informations d'un utilisateur.

- Répondre aux questions

Accédez à http://localhost:8000/check_news/ pour répondre aux questions.