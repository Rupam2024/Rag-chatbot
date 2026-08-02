from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuration

CHROMA_DB_PATH = "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load Embeddings
def load_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return embeddings

# Load Vector Database

def load_vector_db():

    embeddings = load_embeddings()

    vector_db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    return vector_db
