import streamlit as st
import pandas as pd
import zipfile
import os
from utils.file_processor import extract_csv_from_zip
from utils.csv_merger import merge_csv_files
from components.file_uploader import file_uploader
from components.download_button import download_button

def main():
    st.title("CSV Merger from ZIP Files")
    
    uploaded_files = file_uploader()
    
    if st.button("Merge CSV Files"):
        if uploaded_files:
            # Process the uploaded ZIP files and extract CSV files
            csv_files = []
            for uploaded_file in uploaded_files:
                csv_files.extend(extract_csv_from_zip(uploaded_file))
            
            if csv_files:
                # Merge the CSV files into a single DataFrame
                merged_df = merge_csv_files(csv_files)
                
                # Save the merged DataFrame to an XLS file
                output_file = "merged_output.xlsx"
                merged_df.to_excel(output_file, index=False)
                
                # Provide a download button for the merged XLS file
                download_button(output_file)
            else:
                st.error("No CSV files found in the uploaded ZIP files.")
        else:
            st.error("Please upload at least one ZIP file.")

if __name__ == "__main__":
    main()