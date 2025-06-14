# Fusion et analyse de fichiers CSV

Cette application Streamlit permet de fusionner des fichiers CSV contenus dans des archives ZIP et d'effectuer des analyses spécifiques.

## Fonctionnalités

- Upload de fichiers ZIP contenant des fichiers CSV
- Fusion des fichiers CSV avec les paramètres suivants :
  - Encodage : ISO-8859-1
  - Séparateur : ;
  - Délimiteur de texte : "
- Génération d'un fichier Excel avec les feuilles :
  - "Export" : contient toutes les données fusionnées
  - "Moyenne conso DATA" : analyse de la consommation de données par utilisateur

## Installation

```bash
pip install -r requirements.txt
```

## Exécution

```bash
streamlit run app.py
```