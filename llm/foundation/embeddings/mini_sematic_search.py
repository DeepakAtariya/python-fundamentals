from index import cosine_similarity, embed

# A tiny "knowledge base" — pretend these are FAQ entries
documents = [
    "To reset your password, click 'Forgot Password' on the login page.",
    "Our refund policy allows returns within 30 days of purchase.",
    "Premium subscribers get priority customer support and advanced features.",
    "We accept credit cards, PayPal, and bank transfers.",
    "Shipping typically takes 3-5 business days within the country.",
    "International shipping is available and takes 7-14 business days.",
    "You can cancel your subscription anytime from account settings.",
    "Our office hours are 9 AM to 6 PM Monday through Friday.",
    "Two-factor authentication adds an extra security layer to your account.",
    "Bulk orders over $500 qualify for a 10% discount.",
]

# Step 1: Embed all documents ONCE (in real systems, store in a vector DB)
print("Embedding documents...")
doc_embeddings = [embed(doc) for doc in documents]
print(f"Embedded {len(doc_embeddings)} documents.\n")

# Step 2: Search function
def search(query, top_k=3):
    query_vec = embed(query)
    scores = [
        (cosine_similarity(query_vec, doc_vec), doc)
        for doc_vec, doc in zip(doc_embeddings, documents)
    ]
    scores.sort(reverse=True)
    return scores[:top_k]

# Step 3: Try real-world queries
test_queries = [
    "How do I get my money back?",
    "I forgot how to log in",
    "When will my package arrive?",
    "How do I make my account more secure?",
    "Are there any deals for big orders?",
]

for q in test_queries:
    print(f"Query: {q}")
    for score, doc in search(q, top_k=2):
        print(f"  {score:.4f}  {doc}")
    print()