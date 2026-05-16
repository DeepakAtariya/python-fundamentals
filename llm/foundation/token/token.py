# Get the encoding used by GPT-4
from tiktoken import encoding_for_model 

enc = encoding_for_model("gpt-4")

text = "Tokenization is fascinating!"
tokens = enc.encode(text)
print(f"Text: {text}")
print(f"Token count: {len(tokens)}")
print(f"Token IDs: {tokens}")

# Decode each token back to its string to see what they look like
for token_id in tokens:
    print(f"  {token_id} -> '{enc.decode([token_id])}'")
    

