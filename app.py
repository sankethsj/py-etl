import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Py-ETL",
    page_icon=":snake:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# weired state management
if "db_conn_exists" not in st.session_state:
    st.session_state["db_conn_exists"] = False
if "conn" not in st.session_state:
    st.session_state["conn"] = None
if "engine" not in st.session_state:
    st.session_state["engine"] = None
if "schema_name" not in st.session_state:
    st.session_state["schema_name"] = None
if "table_name" not in st.session_state:
    st.session_state["table_name"] = None
if "db_name" not in st.session_state:
    st.session_state["db_name"] = None

# Title
st.title("Py-ETL")
st.caption("A simple ETL tool to load data from Excel/CSV file to Database")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Read the file
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # Display the data
    st.subheader("Data Preview:")
    st.dataframe(df)
    
    # Display data analysis
    st.write("Data Analysis:")
    st.write("Missing Values in Each Column:")
    st.write(df.isnull().sum())
    st.write("Basic Info about data:")
    st.write(df.info())

    # Database connection details
    st.subheader("Database Connection Details")
    db_url = st.text_input("Database URL", "localhost")
    st.session_state.db_name = st.text_input("Database Name", "pulse_db")
    db_user = st.text_input("Username", "postgres")
    db_password = st.text_input("Password", type="password")

    db_connect = st.button("Connect to Database")
    if db_connect:
        if db_url == "" or st.session_state.db_name == "" or db_user == "" or db_password == "":
            st.error("Please fill all the fields!")
            st.stop()

        conn_str = f"postgresql://{db_user}:{db_password}@{db_url}/{st.session_state.db_name}"
        engine = create_engine(conn_str)
        conn = engine.connect()
        st.session_state.conn = conn
        st.session_state.engine = engine
        st.session_state.db_conn_exists = True
        st.success("Connected to the database successfully!")

    if st.session_state.db_conn_exists:
        st.write(f"Connected to the database : {st.session_state.db_name}")

# Fetch schemas
if st.session_state.db_conn_exists:
    schemas = pd.read_sql(
        "SELECT schema_name FROM information_schema.schemata", st.session_state.conn
    )
    schema_name = st.selectbox(
        "Select Schema",
        schemas["schema_name"],
        key="schema",
    )
    st.session_state["schema_name"] = schema_name

# Fetch tables based on selected schema
if st.session_state.schema_name:
    tables = pd.read_sql(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{st.session_state.schema_name}'",
        st.session_state.conn,
    )
    table_name = st.selectbox("Select Table", tables["table_name"], key="table")
    st.session_state["table_name"] = table_name

    # Display row count of the selected table
    if table_name:
        row_count = pd.read_sql(f"SELECT COUNT(*) FROM {st.session_state.schema_name}.{table_name}", st.session_state.conn).iloc[0, 0]
        st.write(f"Rows count in table {table_name}: {row_count}")

# load data into table
if (
    st.session_state.schema_name
    and st.session_state.table_name
    and st.button("Load Data into Database")
):
    try:
        # Insert data into the selected table
        rows_affected = df.to_sql(
            table_name,
            st.session_state.engine,
            schema=schema_name,
            if_exists="replace",
            index=False,
        )
        st.success(
            f"Data loaded into {schema_name}.{table_name} successfully! Total of {rows_affected} rows upserted"
        )
    except Exception as e:
        st.error(f"An error occurred: {str(e.__dict__['orig'])}")
