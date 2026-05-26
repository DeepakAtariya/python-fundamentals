from sklearn.cluster import KMeans
from index import embed
import numpy as np

# Pretend these are customer feedback messages
feedback = [
    # Product quality cluster (you "know" but the algorithm doesn't)
    "The product broke after one week of use",
    "Quality is terrible, fell apart immediately",
    "Stopped working within days, very disappointed",

    # Shipping cluster
    "Package arrived two weeks late",
    "Delivery took forever, awful experience",
    "Still waiting for my order after 3 weeks",

    # Customer service cluster
    "Support team was incredibly helpful",
    "Customer service resolved my issue quickly",
    "Agent was patient and solved everything",

    # Pricing cluster
    "Way too expensive for what you get",
    "Prices have gone up too much lately",
    "Not worth the cost honestly",
]

# Step 1: Embed everything
print("Embedding feedback...")
embeddings = np.array([embed(text) for text in feedback])
print(f"Embeddings matrix shape: {embeddings.shape}")
# shape will be (12, 384) — 12 texts, each 384-dimensional

# Step 2: Cluster into 4 groups
# KMeans will pick 4 "center points" in 384-D space
# and assign each text to its nearest center
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(embeddings)

# Step 3: Print results grouped by cluster
print(f"\nLabels assigned: {labels}\n")
for cluster_id in range(4):
    print(f"--- Cluster {cluster_id} ---")
    for text, label in zip(feedback, labels):
        if label == cluster_id:
            print(f"  • {text}")
    print()
    

'''python

# Pseudocode
for cluster_id in unique_clusters:
    cluster_texts = [t for t, l in zip(texts, labels) if l == cluster_id]
    label = llm_call(f"""
    Here are texts that were grouped together:
    {cluster_texts}

    Give this cluster a short 2-4 word label that captures the common theme.
    """)
    print(f"Cluster {cluster_id}: {label}")

'''
