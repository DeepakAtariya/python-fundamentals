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

# text = "hello"
# vec = embed(text)

# print(f"Text: {text}")
# print(f"Shape: {vec.shape}")
# print(f"Type: {type(vec)}")
# print(f"Magnitude: {np.linalg.norm(vec):.4f}")
# print(f"First 10 values: {vec[:10]}")
# print(f"Min value: {vec.min():.4f}")
# print(f"Max value: {vec.max():.4f}")
# print(f"Mean value: {vec.mean():.4f}")


