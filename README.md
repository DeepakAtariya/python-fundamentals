<div align="center">

# Python Fundamentals

**The Python a backend engineer actually gets asked about — written out, explained, and runnable.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Topics](https://img.shields.io/badge/Topics-Core%20Python%20%7C%20DSA-orange)](#whats-inside)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

</div>

---

Not a tutorial series and not a cheat sheet. These are working notes: the Python
language features that keep showing up in real backend code and real interviews, each
one written down until it was genuinely understood — with the gotchas that bite people
in production kept in, not smoothed over.

Most files are deliberately heavy on commented-out experiments. That's the point: the
reasoning is the content, not just the final answer.

## What's inside

### Core Python — the language itself

| File | Covers |
|------|--------|
| [`python_fundamentals.py`](core_python/python_fundamentals.py) | Types and built-in collections, comprehensions with conditionals, `**kwargs` and building URLs from them, a small `APIClient` class with custom exceptions and `__repr__` |
| [`decorator.py`](core_python/decorator.py) | Writing decorators from scratch — `*args`/`**kwargs` forwarding, why `functools.wraps` matters, and a working `@timer` |
| [`generators_and_terators.py`](core_python/generators_and_terators.py) | `yield`, batch processing a stream, and eager vs lazy — the list comprehension that costs 80MB next to the generator that costs 120 bytes |
| [`context_managers.py`](core_python/context_managers.py) | `__enter__` / `__exit__`, why guaranteed cleanup matters for DB connections and API sessions, and what `with` is really doing |
| [`collections_modules.py`](core_python/collections_modules.py) | `defaultdict`, `Counter`, `OrderedDict`, `deque`, `namedtuple` — and how they're built on `dict`'s hash table, down to `__missing__` |
| [`advanced_oops.py`](core_python/advanced_oops.py) | Dunder methods (`__eq__`, `__call__`, `__repr__`), `@property` for controlled access, frozen dataclasses, `__slots__`, read-only attributes, and the mutable-default-argument trap |

**A few of the traps covered**

- The mutable default argument — one `{}` created at class-definition time, silently shared by every instance
- `functools.wraps`, without which your decorated function loses its own `__name__`
- Why a `(x**2 for x in ...)` generator and a `[x**2 for x in ...]` list differ by six orders of magnitude in memory
- Why `defaultdict` doesn't raise `KeyError` — it overrides exactly one method

### DSA — patterns, not puzzle collections

Each solution is written for the *technique*, with the problem statement and the
reasoning kept inline.

| File | Problem | Pattern |
|------|---------|---------|
| [`two_sum.py`](dsa/two_sum.py) | Two Sum | Hash map for complement lookup |
| [`valid_paranthese.py`](dsa/valid_paranthese.py) | Valid Parentheses | Stack matching |
| [`anagram.py`](dsa/anagram.py) | Valid Anagram | Frequency table comparison |
| [`group_anagram.py`](dsa/group_anagram.py) | Group Anagrams | `defaultdict` keyed by a canonical signature |
| [`self_product.py`](dsa/self_product.py) | Product of Array Except Self | Prefix and suffix products, no division |
| [`347_top_k_elements.py`](dsa/347_top_k_elements.py) | Top K Frequent Elements | Counting plus a heap |

## Running it

No dependencies — standard library only.

```bash
git clone https://github.com/DeepakAtariya/python-fundamentals.git
cd python-fundamentals
```

Both folders use an `index.py` as a scratch entry point: uncomment the import for the
module you want and run it.

```bash
python -m core_python.index    # core_python/index.py selects the module
cd dsa && python index.py      # dsa/index.py does the same
```

Or just run a file directly:

```bash
python core_python/decorator.py
```

Much of the code is intentionally commented out so you can uncomment one block at a
time and watch what changes. Reading top to bottom works better than running it all.

## Repo map

```
core_python/
  python_fundamentals.py       types, comprehensions, kwargs, a small API client
  decorator.py                 decorators from scratch, @timer
  generators_and_terators.py   yield, laziness, memory
  context_managers.py          __enter__ / __exit__
  collections_modules.py       defaultdict, Counter, deque, namedtuple + internals
  advanced_oops.py             dunders, @property, dataclasses, __slots__
  index.py                     entry point — uncomment what you want to run
dsa/
  two_sum.py  valid_paranthese.py  anagram.py
  group_anagram.py  self_product.py  347_top_k_elements.py
  index.py                     entry point
```

## Related

LLM engineering notes — tokenization, embeddings, the chat completion API and a
provider-agnostic wrapper — live in a separate repo:

**→ [Learn LLM with Atariya](https://github.com/DeepakAtariya/learn-llm-with-atariya)**

## Contributing

If an explanation here is wrong or unclear, that's worth an issue. Corrections welcome.

## License

[MIT](LICENSE) © Deepak Atariya
