def extract_zip_files(zip_files):
    import zipfile
    import os

    extracted_files = []
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall("extracted")
            extracted_files.extend(zip_ref.namelist())
    return extracted_files

def read_csv_files(csv_files):
    import pandas as pd

    dataframes = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dataframes.append(df)
    return dataframes

def merge_dataframes(dataframes):
    import pandas as pd

    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df

def save_to_excel(dataframe, output_file):
    import pandas as pd

    dataframe.to_excel(output_file, index=False)