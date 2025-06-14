import streamlit as st
import pandas as pd
import zipfile
import os
from utils import extract_zip, merge_csv_to_xls

def main():
    st.title("Fusion de fichiers CSV")
    
    # Zone de dépôt des fichiers
    uploaded_files = st.file_uploader("Déposez vos fichiers ZIP ici", type=["zip"], accept_multiple_files=True)
    
    if st.button("Démarrer la fusion"):
        if uploaded_files:
            # Créer un dossier temporaire pour extraire les fichiers ZIP
            temp_dir = "temp_extracted"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extraire les fichiers ZIP
            for uploaded_file in uploaded_files:
                extract_zip(uploaded_file, temp_dir)
            
            # Fusionner les fichiers CSV
            merged_file_path = merge_csv_to_xls(temp_dir)
            
            # Bouton de téléchargement
            with open(merged_file_path, "rb") as f:
                st.download_button("Télécharger le fichier XLS fusionné", f, file_name="fichier_fusionne.xlsx")
            
            # Nettoyer le dossier temporaire
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                os.remove(file_path)
            os.rmdir(temp_dir)
        else:
            st.warning("Veuillez télécharger au moins un fichier ZIP.")

if __name__ == "__main__":
    main()