import os
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuration

CSV_PATH = "csv_path_location"
CHROMA_DB_PATH = "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load Dataset

def load_dataset(csv_path):
    """
    Load CSV dataset.
    """

    try:
        df = pd.read_csv(csv_path)

        print(f"\n Dataset Loaded Successfully")
        print(f" Rows: {df.shape[0]}")
        print(f" Columns: {df.shape[1]}")

        return df

    except Exception as e:
        print(f" Error loading dataset: {e}")
        raise


