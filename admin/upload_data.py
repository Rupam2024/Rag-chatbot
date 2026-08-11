import os
import shutil
import streamlit as st
import pandas as pd

from config import (
    CSV_FILE,
    DATA_DIR
)

# Import your ingest function
from vectorstore.ingest import main as rebuild_vector_db

# Save Uploaded File

def save_uploaded_file(uploaded_file):

    try:

        destination = os.path.join(
            DATA_DIR,
            uploaded_file.name
        )

        with open(
            destination,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        return destination

    except Exception as e:

        st.error(
            f"Upload Error: {e}"
        )

        return None

# Validate CSV

def validate_csv(file_path):

    try:

        df = pd.read_csv(file_path)

        if len(df) == 0:

            return False, "CSV is empty"

        return True, df

    except Exception as e:

        return False, str(e)

# Replace Existing Dataset

def replace_dataset(new_file_path):

    try:

        shutil.copy(
            new_file_path,
            CSV_FILE
        )

        return True

    except Exception as e:

        st.error(
            f"Replace Error: {e}"
        )

        return False

# Rebuild ChromaDB

def rebuild_database():

    try:

        rebuild_vector_db()

        return True

    except Exception as e:

        st.error(
            f"Rebuild Error: {e}"
        )

        return False

# Dataset Summary

def show_dataset_summary(df):

    st.subheader(
        "Dataset Summary"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        len(df)
    )

    col2.metric(
        "Columns",
        len(df.columns)
    )

    col3.metric(
        "Missing Values",
        int(df.isna().sum().sum())
    )

    st.dataframe(
        df.head(),
        use_container_width=True
    )

# Main Upload Page

def render_upload_page():

    st.title(
        "Admin Panel"
    )

    st.info(
        "Upload a new pharmaceutical dataset and rebuild the vector database."
    )

    uploaded_file = st.file_uploader(

        "Upload CSV",

        type=["csv"]
    )

    if uploaded_file:

        temp_file = save_uploaded_file(
            uploaded_file
        )

        valid, result = validate_csv(
            temp_file
        )

        if not valid:

            st.error(result)

            return

        df = result

        show_dataset_summary(df)

        st.divider()

        if st.button(
            "Replace Current Dataset"
        ):

            if replace_dataset(
                temp_file
            ):

                st.success(
                    "Dataset Updated Successfully"
                )

        if st.button(
            "Rebuild Vector Database"
        ):

            with st.spinner(
                "Creating Embeddings..."
            ):

                status = rebuild_database()

            if status:

                st.success(
                    "Vector Database Rebuilt Successfully"
                )

# Standalone Testing

if __name__ == "__main__":

    render_upload_page()
