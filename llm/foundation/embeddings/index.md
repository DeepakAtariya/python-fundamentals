# Embeddings
### Simple meaning is Embeddings defines the meaning for models

## What is embedding ?

Earlier, we studied tokens, which converts string to integers `hello -> 9906` which does not tell the model what `hello` means. For model it is just a index.

So how does the model know that "king" and "queen" are related, but "king" and "refrigerator" aren't?

every token ID gets mapped to a vector — a list of numbers — and these vectors are positioned in a high-dimensional space such that semantically similar tokens have similar vectors.

**That vector is called an embedding.** 

A concrete example
Suppose embeddings were just 3-dimensional (real ones are 768, 1536, or 3072 dimensions, but bear with me):

```
"king"   → [0.8, 0.2, 0.6]
"queen"  → [0.7, 0.3, 0.6]
"man"    → [0.8, 0.1, 0.1]
"woman"  → [0.7, 0.2, 0.1]
"apple"  → [0.1, 0.9, 0.4]
```

Notice:

 - king and queen have very similar vectors → they're "close" in this 3D space
 - king and man share the first dimension high → maybe that dimension encodes "royalty/power level" or "human-ness"
 - apple is far from all of them → different concept

This is the magic: meaning is encoded as geometric proximity in vector space. Concepts that are similar in meaning end up physically near each other in this high-dimensional space.

The famous example
The classic demonstration:

```
vector("king") - vector("man") + vector("woman") ≈ vector("queen")
```
The model has learned the "gender" relationship as a direction in space. You can do arithmetic on meanings.

This isn't programmed by hand. It emerges naturally when you train the model on huge amounts of text — words that appear in similar contexts end up with similar vectors.

## Why high-dimensional?

Real embedding spaces have hundreds or thousands of dimensions:

 - OpenAI's `text-embedding-3-small`: 1536 dimensions
 - OpenAI's `text-embedding-3-large`: 3072 dimensions
 - Cohere's models: typically 1024 dimensions

### Why so many? Because language has many dimensions of meaning. A word like "bank" has:

 - Financial vs. river meaning
 - Verb vs. noun usage
 - Formal vs. casual register
 - Singular vs. plural
 - … and hundreds of other subtle distinctions

Each dimension captures some learned feature. You can't visualize 1536D space, but the math works the same as 2D or 3D.

### Measuring similarity — cosine similarity

If two embeddings are vectors, how do we measure how "similar" they are?

The standard answer: cosine similarity — the cosine of the angle between the two vectors.

`cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)`

Values range from -1 to 1:

 - 1.0 → vectors point in the exact same direction → identical meaning
 - 0.0 → perpendicular → unrelated
 - -1.0 → opposite directions → opposite meaning (rare in practice)

Why cosine, not Euclidean distance? Because direction matters more than magnitude for meaning. "The cat sat on the mat" and "Cat sat mat" should be similar in meaning even if one vector is longer than the other. Cosine ignores magnitude.

In practice, for OpenAI embeddings:

 - `> 0.8` → very similar (likely paraphrases or about the same topic)
 - `0.5` – 0.8 → related (same domain or theme)
 - `< 0.3` → mostly unrelated

# Two distinct uses of embeddings

This trips up most people learning AI. There are two different places embeddings show up, and they're related but not the same:

### Use case 1 : Embeddings inside the model (token embeddings)

When you call GPT-4 with a prompt:

```
"Hello world"
    ↓
tokens: [9906, 1917]
    ↓
each token → looked up in an embedding table → vector
    ↓
[9906] → [0.21, -0.45, 0.78, …, 0.12]  (1536-dim)
[1917] → [0.34, 0.12, -0.66, …, 0.91]  (1536-dim)
    ↓
these vectors flow into the transformer
    ↓
the transformer thinks and generates output
```

These are **token embeddings**, and they're an internal implementation detail of the LLM. You don't see them, you don't call an API for them — they exist inside the model.

### Use case 2: Embeddings as a standalone API (text/sentence embeddings)

OpenAI and others also offer dedicated embedding endpoints. You send entire sentences or documents, and you get back one vector per input representing the meaning of the whole text.

```
openai.embeddings.create(
    model="text-embedding-3-small",
    input="The cat sat on the mat"
)
# returns: a single 1536-dim vector for the whole sentence
```

This is what powers:

 - Semantic search ("find documents similar to this query")
 - RAG systems (retrieve relevant chunks based on similarity)
 - Clustering (group similar documents together)
 - Classification (is this email spam? — measure similarity to spam examples)
 - Recommendation (find articles similar to ones you liked)


| Use case | How |
|----------|-----|
| **Duplicate detection** | User submits a support ticket. Compare its embedding to existing tickets. If similarity > 0.9, flag as duplicate → "We've seen this issue before, here's the answer." |
| **Semantic search** | Index every doc as an embedding. User query → embedding → find top-K most similar docs by cosine. |
| **FAQ matching** | Pre-embed all FAQ answers. New user question → embedding → return the closest FAQ. |
| **Recommendation** | "Users who liked this article also read…" — recommend articles whose embeddings are near the current one. |
| **Plagiarism / paraphrase detection** | Compare student essays to a corpus. High similarity = suspicious. |
| **Customer feedback clustering** | Embed thousands of reviews → cluster by similarity → discover themes without manually reading them all. |
| **Anomaly detection** | Embed log lines. New log with low similarity to all historical logs = potentially novel error. |
| **Chatbot routing** | "Is this user asking about billing or technical?" — embed the message, compare to category exemplars. |

**Engineer takeaway**: Cosine similarity is not just a math curiosity. It's the foundation of an entire class of product features. Once you can map text → vector → similarity score, dozens of features become possible without ever training a custom ML model.

## Why do we use standalone embeddings?

### Reason 1 : It doesn't scale
"send the entire docs corpus to GPT-4."
What is "the entire docs corpus"? For most companies:

 - 10,000 internal docs
 - Each averaging 5,000 words
 - Total: 50 million words ≈ 65+ million tokens

No model has a 65 million token context window. It physically cannot fit. Even Gemini's 1M context maxes out at <2% of this corpus.
Embeddings flip the problem:

 - Embed all 10,000 docs once, store in a vector DB
 - At query time: embed only the user's question (~10 tokens)
 - Vector DB returns top 5 most similar chunks (~2,500 tokens total)
 - Send only those to GPT-4

You went from "impossible" → "small, fast, cheap query."

### Reason 2 : Latency

Even if the entire corpus did fit (small docs, big model), the latency would be brutal:

 - Time-to-first-token scales with input length
 - Sending 65M tokens (hypothetically) = 30+ seconds before any output
 - With embeddings: vector search is sub-100ms, then a small LLM call

Users won't wait 30 seconds. They will wait 1 second.

### Reason 3 : Cost

Doing this for every search query:

 - Naive approach: pay for 65M input tokens × every query → financially impossible
 - Embeddings approach: pay tiny one-time embedding cost (~$0.02/million tokens), then pennies per query

For a real product with thousands of queries/day, this is the difference between a $50/month bill and a $50,000/month bill.

### Reason 4: Quality — "Lost in the Middle"
Even if you stuffed everything into the context, GPT-4 wouldn't use it well. Research consistently shows LLMs:

 - Pay attention to the beginning and end of long contexts
 - Lose information buried in the middle
 - Get distracted by irrelevant content

Sending only the 5 most relevant chunks actually produces better answers than sending everything. Less is more.

### Reason 5: Freshness / updates

If your docs change daily:
 - Naive approach: every query re-reads the full corpus → wastes everything
 - Embeddings approach: re-embed only the changed docs (incremental) → cheap

### Reason 6: Your point — control
You can choose chunking strategy, hybrid search (combine keyword + semantic), re-ranking, filtering by metadata (only docs from 2026, only engineering docs, etc.). You can't do any of this when "the LLM is the search engine."

The mental model to lock in

```Embeddings + vector search is the canonical pattern for "search over a corpus." Stuffing the corpus into the context window is almost never the right architecture.```

This is the foundation of RAG, and in Month 3 we'll go deep on every piece later — chunking, vector DBs, hybrid search, re-ranking.