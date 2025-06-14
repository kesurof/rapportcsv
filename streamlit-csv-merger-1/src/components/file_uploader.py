import streamlit as st
import zipfile
import os

def file_uploader():
    st.title("CSV Merger")
    st.write("Upload one or more ZIP files containing CSV files.")

    uploaded_files = st.file_uploader("Choose ZIP files", type="zip", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall("temp_dir")
                st.success(f"Extracted {uploaded_file.name}")

    if st.button("Merge Files"):
        # Logic to merge files will be implemented in merger.py
        st.write("Merging files...")