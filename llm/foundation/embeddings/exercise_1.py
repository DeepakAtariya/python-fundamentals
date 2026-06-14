from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model (first call downloads ~80MB; subsequent calls are cached)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text: str) -> np.ndarray:
    """Return a numpy array embedding for the given text."""
    return model.encode(text, convert_to_numpy=True)

# Get one embedding and inspect it
vec = embed("I love programming")
print(f"Embedding shape: {vec.shape}")
print(f"First 5 values: {vec[:5]}")
print(f"Vector magnitude (length): {np.linalg.norm(vec):.4f}")