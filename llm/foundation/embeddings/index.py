from sentence_transformers import SentenceTransformer
import numpy as np

# Load once, reuse everywhere
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    """Return embedding as numpy array."""
    return model.encode(text, convert_to_numpy=True)

def cosine_similarity(a, b):
    """Return cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))



