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

def clean_dataset(df):
    """
    Clean and preprocess dataset.
    """

    df = df.copy()

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill NaN values
    df = df.fillna("Not Available")

    # Convert all columns to string
    for col in df.columns:
        df[col] = df[col].astype(str)

    print(f" Cleaned Records: {len(df)}")

    return df

def create_documents(df):
    """
    Convert rows into LangChain Documents.
    """

    documents = []

    for _, row in df.iterrows():

        content = f"""
SKU: {row.get('SKU', '')}

Company: {row.get('Company', '')}

Category: {row.get('Sub Group', '')}

Composition: {row.get('Composition', '')}

Strength: {row.get('Strength', '')}

MRP: {row.get('MRP', '')}

Brand: {row.get('Brand', '')}
"""

        metadata = {
    "sku": str(row.get("SKU", "")),
    "company": str(row.get("Company", "")),
    "category": str(row.get("Sub Group", "")),
    "composition": str(row.get("Composition", "")),
    "strength": str(row.get("Strength", "")),
    "mrp": str(row.get("MRP", "")),
    "brand": str(row.get("Brand", ""))
}

        documents.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    print(f" Documents Created: {len(documents)}")

    return documents

def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return embeddings


# Build ChromaDB

def build_vector_database(documents):

    if os.path.exists(CHROMA_DB_PATH):

        import shutil

        print("Removing old vector database...")

        shutil.rmtree(CHROMA_DB_PATH)

    embeddings = get_embeddings()

    print("Creating vector embeddings...")

    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )

    print("ChromaDB Created Successfully")

    return vector_db


def main():

    print("=" * 50)
    print("DRUG RAG VECTOR DATABASE BUILDER")
    print("=" * 50)

    df = load_dataset(CSV_PATH)

    df = clean_dataset(df)

    documents = create_documents(df)

    build_vector_database(documents)

    print("\n Vector Database Ready!")
    print(" Stored in:", CHROMA_DB_PATH)

if __name__ == "__main__":
    main()





