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

