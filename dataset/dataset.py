import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import pickle
import faiss
from dotenv import load_dotenv

load_dotenv()
def load_en_data():
    """Load Keyword data"""
    if(os.getenv("EN_DATA")):
        data_path = os.environ.get("EN_DATA")
    print("loading data")
    return pd.read_csv(data_path)

def load_en_model():
    """Instantiate a sentence-level DistilBERT model."""
    print('loading en keyword model')
    if(os.getenv("EN_MODEL")):
        model_path = os.environ.get("EN_MODEL")
    model = SentenceTransformer(model_path)
    return model

def load_en_faiss():
    """Load and deserialize the keywords Faiss index."""
    if(os.getenv("EN_FAISS")):
        faiss_path = os.environ.get("EN_FAISS")
    with open(faiss_path, "rb") as h:
        data = pickle.load(h)
    print('loading faiss index')
    return faiss.deserialize_index(data)