from streamlit import file_uploader, button, download_button
import pandas as pd
import zipfile
import os
from utils.file_processor import process_csv_files
from utils.excel_writer import write_to_excel

def merge_files():
    uploaded_files = file_uploader("Déposez vos fichiers ZIP contenant des fichiers CSV", type=["zip"], accept_multiple_files=True)
    
    if button("Démarrer la fusion"):
        if uploaded_files:
            all_data = []
            for uploaded_file in uploaded_files:
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall("temp_dir")
                    csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                    for csv_file in csv_files:
                        data = process_csv_files(os.path.join("temp_dir", csv_file))
                        all_data.append(data)
            
            if all_data:
                merged_data = pd.concat(all_data, ignore_index=True)
                output_file = "Analyse de Parc.xlsx"
                write_to_excel(merged_data, output_file)
                
                with open(output_file, "rb") as f:
                    download_button("Télécharger le fichier Excel", f, file_name=output_file)

            # Clean up temporary files
            for csv_file in os.listdir("temp_dir"):
                os.remove(os.path.join("temp_dir", csv_file))
            os.rmdir("temp_dir")