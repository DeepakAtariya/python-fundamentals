# Token 

When you send text to an LLM, it doesn't see characters or words. It sees tokens — chunks of text that get mapped to integers.Here's the key insight: a token is not a word, not a character, but something in between.
Take the sentence: "Tokenization is fascinating!"

GPT-4 might break this into roughly:

```
["Token", "ization", " is", " fasc", "inating", "!"]
   →        →       →       →         →        →
 [3404,   2860,   374,   13476,    8330,    0] 
```

### Six tokens. Notice:
 - Common words like "is" stay whole (with the leading space)
 - Rare words get split ("fascinating" → "fasc" + "inating")
 - Punctuation is its own token
 - The leading space matters — " is" and "is" are different tokens

### Why does this matter for an engineer?

 - Cost — APIs charge per token. 1000 words ≈ 750 tokens in English, but more like 1500+ tokens for languages like Hindi or Arabic. This has real cost implications.
 - Context window — When the docs say "GPT-4o has a 128k context window," they mean 128,000 tokens, not characters or words.
 - Latency — Models generate one token at a time. Longer outputs = slower.
 - Weird model behavior — Some bugs (like models being bad at counting letters in "strawberry") come straight from tokenization.

## What's the engineering problem with sending a 500-page PDF in one prompt?


Rough math: 500 pages × 500 words/page ≈ 250,000 words ≈ ~330,000 tokens (English).
Real model context windows (2026):

```
GPT-4o: 128k tokens
Claude Sonnet 4.6: 200k tokens
Gemini 1.5 Pro: 1M+ tokens
```

The decision tree is more nuanced than just "split it":

Does it fit? Check token count first (tiktoken for OpenAI, anthropic.count_tokens() for Claude).
Should it fit, even if it can?

  - Cost — input tokens cost real money (~$1–3 per query for huge contexts)
  - Latency — long prompts mean higher time-to-first-token
  - Lossy — the "Lost in the Middle" paper shows models forget content buried in huge contexts


What's the real goal? If user wants Q&A on the PDF → use RAG (Retrieval Augmented Generation). Chunk the PDF, embed the chunks, retrieve only relevant chunks per question, send only those to the LLM. (Coming in Month 3.)

Engineer takeaway: "It fits" is the weakest reason to put data in a prompt. Cost, latency, and retrieval quality all argue for sending less, not more.

## TikToken: Implementation of BPE algorithm

tiktoken is OpenAI's fast, optimized implementation of the specific BPE vocabularies that OpenAI's models use.
Three things often conflated — keep them separate:

 - BPE = the algorithm (general, 1994 compression technique, anyone can implement)
 - The vocabulary = the trained artifact (~100k tokens, specific to each model)

   - GPT-3.5 / GPT-4 → cl100k_base (~100k tokens)
   - GPT-4o / GPT-4o-mini → o200k_base (~200k tokens)
   - Claude, Llama, Gemini each have their own


 - tiktoken = a fast Rust-backed library that ships with OpenAI's vocabularies

 ### Flow

 ```
 BPE (algorithm)
  └── trained on OpenAI's corpus
        └── produces vocabulary file (e.g., cl100k_base)
              └── tiktoken loads & applies it efficiently
```
