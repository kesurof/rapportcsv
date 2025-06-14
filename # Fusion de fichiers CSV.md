# Fusion de fichiers CSV

Cette application Streamlit permet de fusionner des fichiers CSV contenus dans des archives ZIP.

## Fonctionnalités

- Upload de fichiers ZIP contenant des fichiers CSV
- Fusion des fichiers CSV avec les paramètres suivants :
  - Encodage : ISO-8859-1
  - Séparateur : ;
  - Délimiteur de texte : "
- Export au format Excel (fichier "Analyse de Parc.xlsx" avec une feuille nommée "Export")

## Installation

```bash
pip install -r requirements.txt
```

## Exécution

```bash
streamlit run app.py
```