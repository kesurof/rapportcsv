# Streamlit CSV Merger

This project is a Streamlit application that allows users to merge multiple CSV files contained within ZIP files into a single Excel file. The application provides a user-friendly interface for uploading files and downloading the merged output.

## Features

- Upload one or more ZIP files containing CSV files.
- Merge all CSV files with the same structure into a single Excel file.
- Download the merged Excel file named "Analyse de Parc.xlsx".

## Requirements

To run this application, you need to have Python installed along with the required libraries. You can install the necessary packages using the following command:

```
pip install -r requirements.txt
```

## Configuration

The application uses the following settings for processing CSV files:

- **Encoding**: ISO-8859-1
- **Separator**: ;
- **Text Delimiter**: "

These settings can be modified in the `config.py` file if needed.

## Usage

1. Run the application using the command:

   ```
   streamlit run src/app.py
   ```

2. Open the provided URL in your web browser.
3. Drag and drop your ZIP files containing CSV files into the designated area.
4. Click the "Merge" button to start the merging process.
5. Once the process is complete, a download button will appear. Click it to download the merged Excel file.

## Project Structure

```
streamlit-csv-merger
├── src
│   ├── app.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   └── excel_writer.py
│   └── components
│       ├── __init__.py
│       ├── file_uploader.py
│       └── merger.py
├── requirements.txt
├── config.py
└── README.md
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.