import pandas as pd
import zipfile
import io
import streamlit as st

def merge_csv_files(uploaded_files):
    """
    Fusionne les fichiers CSV extraits des fichiers ZIP
    """
    all_dataframes = []
    
    for uploaded_file in uploaded_files:
        try:
            # Lire le fichier ZIP
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                # Lister tous les fichiers CSV dans le ZIP
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                
                for csv_file in csv_files:
                    # Extraire et lire le fichier CSV
                    with zip_ref.open(csv_file) as file:
                        # Lire avec l'encodage ISO-8859-1 et séparateur ;
                        df = pd.read_csv(
                            file,
                            encoding='ISO-8859-1',
                            separator=';',
                            quotechar='"',
                            dtype=str  # Garder tous les types comme string pour éviter les transformations
                        )
                        all_dataframes.append(df)
                        st.info(f"✅ Fichier traité : {csv_file} ({len(df)} lignes)")
                        
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement de {uploaded_file.name}: {str(e)}")
    
    if all_dataframes:
        # Concaténer verticalement tous les DataFrames
        merged_df = pd.concat(all_dataframes, ignore_index=True, sort=False)
        return merged_df
    else:
        return None