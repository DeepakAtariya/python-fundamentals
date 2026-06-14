def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Predict BEFORE running: rank from most similar to least similar
candidates = [
    "I enjoy writing code",
    "Programming is my passion",
    "I had pasta for dinner",
    "Software engineering is a great career",
    "The weather is nice today",
    "I hate programming",  # interesting one — opposite sentiment, same topic
]

query = "I love programming"
query_vec = embed(query)

print(f"Query: {query!r}\n")
results = []
for c in candidates:
    sim = cosine_similarity(query_vec, embed(c))
    results.append((sim, c))

# Sort descending
results.sort(reverse=True)
for sim, text in results:
    print(f"  {sim:.4f}  {text}")       