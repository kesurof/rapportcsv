import pandas as pd
import io

def create_excel_file(dataframe):
    """
    Crée un fichier Excel avec le nom et la feuille spécifiés
    """
    # Créer un buffer en mémoire
    excel_buffer = io.BytesIO()
    
    # Écrire le DataFrame dans le fichier Excel
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        dataframe.to_excel(
            writer,
            sheet_name='Export',
            index=False
        )
    
    # Revenir au début du buffer
    excel_buffer.seek(0)
    
    return excel_buffer.getvalue()