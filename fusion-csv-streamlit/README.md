# Fusion CSV Streamlit

Ce projet est une application Streamlit qui permet de fusionner plusieurs fichiers CSV contenus dans un ou plusieurs fichiers ZIP. Les fichiers CSV doivent avoir les mêmes colonnes, et l'application fusionne toutes les lignes dans un fichier XLS.

## Structure du projet

```
fusion-csv-streamlit
├── src
│   ├── app.py          # Point d'entrée de l'application Streamlit
│   └── utils.py        # Fonctions utilitaires pour la fusion des fichiers CSV
├── requirements.txt     # Dépendances nécessaires pour le projet
└── README.md            # Documentation du projet
```

## Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante :

```
pip install -r requirements.txt
```

## Utilisation

1. Lancez l'application Streamlit avec la commande suivante :

```
streamlit run src/app.py
```

2. Une fois l'application lancée, vous verrez une zone de dépôt pour télécharger vos fichiers ZIP contenant les fichiers CSV.

3. Cliquez sur le bouton pour démarrer la fusion des fichiers CSV.

4. Après la fusion, un bouton de téléchargement apparaîtra pour récupérer le fichier XLS fusionné.

## Auteurs

Ce projet a été développé par [Votre Nom].