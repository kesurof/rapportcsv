from io import BytesIO
import streamlit as st
import pandas as pd

def download_button(dataframe, filename):
    if dataframe is not None:
        # Convert the DataFrame to an Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Merged Data')
        output.seek(0)

        # Create a download button
        st.download_button(
            label="Download Merged XLS",
            data=output,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )