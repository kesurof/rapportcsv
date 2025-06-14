from io import BytesIO
import zipfile
import pandas as pd
import streamlit as st

def upload_zip_files():
    """
    Composant pour uploader des fichiers ZIP contenant des CSV
    """
    st.subheader("📁 Zone de dépôt des fichiers")
    
    uploaded_files = st.file_uploader(
        "Glissez-déposez vos fichiers ZIP ici",
        type=['zip'],
        accept_multiple_files=True,
        help="Uploadez un ou plusieurs fichiers ZIP contenant des fichiers CSV"
    )
    
    return uploaded_files

def extract_csv_from_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as z:
        csv_files = [z.open(name) for name in z.namelist() if name.endswith('.csv')]
        return csv_files

def read_csv_files(csv_files):
    dataframes = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

def merge_zip_files(uploaded_files):
    all_dataframes = []
    for zip_file in uploaded_files:
        csv_files = extract_csv_from_zip(zip_file)
        df = read_csv_files(csv_files)
        all_dataframes.append(df)
    return pd.concat(all_dataframes, ignore_index=True) if all_dataframes else pd.DataFrame()