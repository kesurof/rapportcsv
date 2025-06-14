import streamlit as st
import pandas as pd
import zipfile
import io
import os
import sys

# Ajouter le répertoire src au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.file_uploader import file_uploader
from components.merger import merge_csv_files
from utils.excel_writer import create_excel_file

def main():
    st.title("🔗 Fusion de fichiers CSV")
    st.markdown("---")
    
    # Zone de dépôt des fichiers
    uploaded_files = file_uploader()
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} fichier(s) uploadé(s)")
        
        # Bouton pour démarrer la fusion
        if st.button("🚀 Démarrer la fusion", type="primary"):
            with st.spinner("Fusion en cours..."):
                try:
                    # Fusion des fichiers
                    merged_df = merge_csv_files(uploaded_files)
                    
                    if merged_df is not None and not merged_df.empty:
                        st.success(f"✅ Fusion terminée ! {len(merged_df)} lignes fusionnées")
                        
                        # Création du fichier Excel
                        excel_buffer = create_excel_file(merged_df)
                        
                        # Bouton de téléchargement
                        st.download_button(
                            label="📥 Télécharger Analyse de Parc.xlsx",
                            data=excel_buffer,
                            file_name="Analyse de Parc.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    else:
                        st.error("❌ Aucune donnée à fusionner")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de la fusion : {str(e)}")

if __name__ == "__main__":
    main()