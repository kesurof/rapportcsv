def extract_csv_from_zip(zip_file):
    import zipfile
    import pandas as pd
    from io import BytesIO

    csv_files = []
    with zipfile.ZipFile(zip_file, 'r') as z:
        for file_name in z.namelist():
            if file_name.endswith('.csv'):
                with z.open(file_name) as f:
                    csv_files.append(pd.read_csv(f))
    return csv_files

def merge_csv_files(csv_files):
    if not csv_files:
        return None
    merged_df = pd.concat(csv_files, ignore_index=True)
    return merged_df

def save_to_xls(dataframe, output_file):
    if dataframe is not None:
        dataframe.to_excel(output_file, index=False)