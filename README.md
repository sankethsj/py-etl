# Py-ETL

Py-ETL is a simple ETL (Extract, Transform, Load) tool that allows users to upload an Excel or CSV file, preview the data, analyze it, and load it into a PostgreSQL database.

## Features

- Upload Excel or CSV files
- Preview the uploaded data
- Analyze the data (missing values, basic statistics)
- Connect to a PostgreSQL database
- Select schema and table from the database
- Load data into the selected table

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sankethsj/py-etl.git
    cd py-etl
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Follow the steps in the app:
    - Upload an Excel or CSV file.
    - Preview and analyze the data.
    - Enter the database connection details and connect to the database.
    - Select the schema and table.
    - Load the data into the selected table.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
