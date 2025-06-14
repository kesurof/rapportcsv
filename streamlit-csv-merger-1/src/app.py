import streamlit as st
import zipfile
import os
from utils.file_processor import process_csv_files
from utils.excel_writer import write_to_excel
from components.file_uploader import file_uploader

def main():
    st.title("CSV Merger Application")
    st.write("Upload one or more ZIP files containing CSV files to merge them into a single Excel file.")

    uploaded_files = file_uploader()

    if uploaded_files:
        if st.button("Merge CSV Files"):
            merged_data = process_csv_files(uploaded_files)
            if merged_data is not None:
                output_file = "Analyse de Parc.xlsx"
                write_to_excel(merged_data, output_file)
                st.success(f"Files merged successfully! Download your file below:")
                st.download_button(label="Download Excel File", data=open(output_file, "rb"), file_name=output_file)
            else:
                st.error("No data found in the uploaded files.")

if __name__ == "__main__":
    main()