# Streamlit CSV Merger

This project is a Streamlit application designed to merge multiple CSV files contained within ZIP archives into a single XLS file. The application provides a user-friendly interface for uploading ZIP files, processing the CSV files, and downloading the merged result.

## Features

- Upload one or multiple ZIP files containing CSV files.
- Automatically merge all CSV files with the same columns into a single XLS file.
- Download the merged XLS file directly from the application.

## Project Structure

```
streamlit-csv-merger
├── src
│   ├── app.py                # Main entry point of the Streamlit application
│   ├── utils
│   │   ├── __init__.py       # Marks the utils directory as a Python package
│   │   ├── file_processor.py  # Functions for processing uploaded files
│   │   └── csv_merger.py      # Functions for merging CSV files into XLS
│   └── components
│       ├── __init__.py       # Marks the components directory as a Python package
│       ├── file_uploader.py   # Component for uploading ZIP files
│       └── download_button.py  # Component for downloading the merged XLS file
├── requirements.txt           # Lists the dependencies required for the project
├── config.toml                # Configuration settings for the application
└── README.md                  # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-csv-merger
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Use the file uploader to select and upload your ZIP files containing CSV files.

4. Click the "Merge" button to start the merging process.

5. Once the merging is complete, download the merged XLS file using the provided download button.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.