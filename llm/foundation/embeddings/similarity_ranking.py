from index import cosine_similarity, embed

query = "I love programming"

candidates = [
    "Coding is my favorite hobby",
    "I enjoy writing software",
    "Python is a great language",
    "The pizza was delicious",
    "I hate Mondays",
    "I love programming",            # identical — sanity check
    "I HATE programming",            # opposite sentiment, same topic
    "Programming is terrible",       # opposite sentiment, same topic
    "Soccer is fun to watch",
]

# Predict BEFORE running:
# - Which will score highest?
# - Where will "I HATE programming" rank? Top? Bottom? Middle?

query_vec = embed(query)
results = [(cosine_similarity(query_vec, embed(c)), c) for c in candidates]
results.sort(reverse=True)

print(f"Query: {query!r}\n")
for sim, text in results:
    print(f"  {sim:.4f}  {text}")
    
"""markdown
The ranking — what's surprising and why
The headline result

"I HATE programming" scored 0.8152 — the second-highest in the entire list.

Higher than "Coding is my favorite hobby" (0.7573), higher than "I enjoy writing software" (0.7066). The model thinks "I HATE programming" is more similar to "I love programming" than "Coding is my favorite hobby" is.
This is a real problem if you're building a product, and you need to understand exactly why.
What's actually happening
Embeddings encode topical/semantic overlap, not sentiment alignment. The model breaks down "I love programming" roughly as:

Subject: "I"
Action verb: "love" (emotional, positive)
Object: "programming" (a topic)

When it sees "I HATE programming," three out of four pieces are identical:

Same subject ("I")
Same structural pattern (pronoun + verb + topic)
Same topic ("programming")
Only the sentiment flipped

So the model rates them very similar — because they ARE very similar, structurally and topically. The opposite-direction sentiment is just one feature among many, and it's outweighed by everything else.
Notice the ranking pattern
Look at how the scores cluster:
1.0000  I love programming                  ← exact match
0.8152  I HATE programming                  ← same topic + structure
0.7573  Coding is my favorite hobby         ← same topic, different words
0.7066  I enjoy writing software            ← related topic
0.6561  Programming is terrible             ← same topic, different structure
─────── (gap) ───────
0.5301  Python is a great language          ← related topic
0.3166  Soccer is fun to watch              ← unrelated topic
0.2761  I hate Mondays                      ← totally unrelated
0.1357  The pizza was delicious             ← maximally different
The big jump in similarity is between "Programming is terrible" (0.65) and "Python is a great language" (0.53). Above that line: everything is on the programming topic. Below: different topics.
That gap is the "topic boundary." Embeddings drew it cleanly. Sentiment? Not so much.
Why even "Programming is terrible" scores lower than "I HATE programming"
This is subtle. "I HATE programming" scored 0.81; "Programming is terrible" scored 0.66. Same sentiment (negative), same topic. Why the gap?
Because sentence structure matters too. "I HATE programming" has the same "I [verb] programming" template as the query. "Programming is terrible" has a different structure. The model picked up on that structural similarity as another vote for "these are alike."
This is why embedding-based search is sensitive to phrasing, not just content. Two ways of expressing the same idea can score noticeably differently.
The engineering consequences — this is where it gets real
You just discovered, hands-on, why building search/RAG systems on naive embeddings has known failure modes. Here are the real product implications:
Failure mode 1: Customer support nightmare
Imagine you're building a support search system. A user types:

"My product works great"

Your embedding-based search returns top hits like:

"My product is broken" (high similarity!)
"My product stopped working" (high similarity!)
"Product quality issues" (high similarity!)

All terrible matches for someone giving positive feedback. Sentiment-flipped versions look almost identical to the query.
Failure mode 2: Recommendation reversal
You recommend articles "similar to this one." User reads a positive review of a movie. Your system recommends the negative review of the same movie. Same topic, opposite sentiment, very high embedding similarity. Disaster.
Failure mode 3: Search relevance
User searches: "safe for kids". Your embedding search returns:

"Not safe for kids" (high similarity — same topic structure)
"Unsafe for children" (high similarity)

You've literally surfaced the opposite of what they asked for.
Failure mode 4: Negation in general
Embeddings are notoriously bad at negation. "I want pizza" and "I don't want pizza" embed very similarly. The word "don't" is just one small signal swamped by all the other tokens.
How production systems handle this
You're now seeing why "just embed everything and find nearest neighbors" isn't enough for serious products. Real systems use several strategies:
1. Hybrid search
Combine semantic similarity (embeddings) with keyword search (BM25). Keywords catch exact negations and specific terms that embeddings miss.
Final score = 0.5 × embedding_similarity + 0.5 × keyword_match
We'll cover this in Month 3.
2. Re-ranking with a cross-encoder
After getting top candidates by embedding similarity (fast, approximate), run them through a more expensive model that reads the query AND candidate together and scores their actual relevance. Cross-encoders are much better at sentiment and negation. We'll cover this in Month 3 too.
3. LLM-as-judge for final filtering
After retrieval, ask an LLM "does this result actually answer the query?" Slow and expensive, but accurate.
4. Specialized embeddings
Some embedding models are trained to be sensitive to sentiment or negation. They're more expensive but better for these cases.
5. Query rewriting
Before searching, use an LLM to rewrite the query into something more searchable. "Safe for kids" might be rewritten as "child-appropriate content suitable for young viewers" to bias toward positive framings.
What this isn't
It's not that embeddings are "broken" or "useless." They're great at:

Finding topically relevant content
Discovering themes in data (clustering, as you'll see in Exercise 4)
Cheap, fast first-pass filtering
Handling vocabulary differences ("car" ↔ "vehicle" ↔ "automobile")

Just don't expect them to be your only retrieval mechanism. They're step 1 in a pipeline, not the whole pipeline.
The most important interview question this prepares you for
If an interviewer asks: "What are the limitations of embedding-based search?" — the answer most candidates give is "they're expensive" or "they have a context limit." Both are wrong / not the real issue.
The right answer (which you can now give from experience):

"Embeddings capture topical and semantic similarity well, but they're weak at negation, sentiment, and fine-grained distinctions. A query for 'safe for kids' will return documents about 'not safe for kids' with high similarity. Production systems combine embedding search with keyword search (hybrid retrieval) and use cross-encoder re-rankers for the final ranking to handle these cases."

You now have that answer in your hands because you literally ran the experiment.
Engineer takeaway
The single biggest reason RAG systems fail in production is that builders treat embeddings as if they were magic semantic-meaning detectors. They're not. They're "topic + structure" detectors with a sentiment blind spot.
The right mental model: embeddings are fast, fuzzy first-pass filters. They get you from "1 million documents" down to "top 50 candidates." After that, you need other techniques (keyword filters, re-ranking, LLM verification) for the final precision.
"""