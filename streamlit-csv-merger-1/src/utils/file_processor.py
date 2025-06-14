import os
import pandas as pd
import zipfile

def process_zip_files(zip_file_paths):
    all_dataframes = []
    
    for zip_file_path in zip_file_paths:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
            for csv_file in csv_files:
                with zip_ref.open(csv_file) as file:
                    df = pd.read_csv(file, encoding='ISO-8859-1', sep=';', quotechar='"')
                    all_dataframes.append(df)
    
    if all_dataframes:
        merged_dataframe = pd.concat(all_dataframes, ignore_index=True)
        return merged_dataframe
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no CSV files were found