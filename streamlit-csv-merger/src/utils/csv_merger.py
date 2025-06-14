def merge_csv_files(csv_files):
    import pandas as pd

    # Initialize an empty DataFrame to hold the merged data
    merged_df = pd.DataFrame()

    # Loop through each CSV file and append its content to the merged DataFrame
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    return merged_df

def save_to_xls(merged_df, output_file):
    # Save the merged DataFrame to an XLS file
    merged_df.to_excel(output_file, index=False)