"""
Multi-provider chat wrapper.

The design rule this file demonstrates:
    ChatApp (the REPL) depends ONLY on neutral types — Message, Usage — and the
    Provider interface. It never touches a vendor's SDK types or response shape.
    Adding a new provider = one new Provider subclass + one line in the factory.
    ChatApp does NOT change. That is the entire point of Week 4.

Run:
    PROVIDER=groq   python multi_provider_chat.py      # default
    PROVIDER=ollama python multi_provider_chat.py      # needs Ollama running locally
"""

import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful assistant and this is a CLI based interface. "
    "Please limit the output to 50 words."
)

# Your neutral message format — a plain dict, not any vendor's type.
Message = dict[str, str]  # {"role": "system"|"user"|"assistant", "content": str}


# ---------- neutral types (yours, not any vendor's) ----------
@dataclass
class Usage:
    input_tokens: int
    output_tokens: int

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


# ---------- provider interface ----------
class Provider(ABC):
    @abstractmethod
    def stream(self, messages: list[Message]) -> Iterator[str]:
        """Yield text pieces as they arrive from the model."""
        ...

    @abstractmethod
    def last_usage(self) -> Optional[Usage]:
        """Usage for the most recent stream() call, available once it's exhausted."""
        ...


# ---------- one adapter for ALL OpenAI-compatible endpoints ----------
class OpenAICompatibleProvider(Provider):
    """Works for Groq, OpenAI, Together, and local Ollama's /v1 endpoint."""

    def __init__(self, api_key: Optional[str], base_url: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self._usage: Optional[Usage] = None

    def stream(self, messages: list[Message]) -> Iterator[str]:
        self._usage = None  # reset for this call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # plain dicts are accepted
            stream=True,
            stream_options={"include_usage": True},
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
            # usage arrives on the final chunk (empty choices); translate it
            # from the vendor's shape into YOUR neutral Usage here.
            if chunk.usage:
                self._usage = Usage(
                    input_tokens=chunk.usage.prompt_tokens,
                    output_tokens=chunk.usage.completion_tokens,
                )

    def last_usage(self) -> Optional[Usage]:
        return self._usage


# To add a genuinely different vendor (e.g. Anthropic), you would write:
#
#   class AnthropicProvider(Provider):
#       def stream(self, messages):
#           # - pull the system message out of `messages` into a top-level param
#           # - call client.messages.stream(...)
#           # - yield event.delta.text
#           # - translate response.usage.input_tokens/output_tokens -> Usage
#       def last_usage(self): ...
#
# ...and add one branch in make_provider(). ChatApp stays untouched — that is
# the proof your abstraction actually abstracts.


def make_provider(name: str) -> Provider:
    name = name.lower()
    if name == "groq":
        return OpenAICompatibleProvider(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            model=os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b"),
        )
    if name == "ollama":
        return OpenAICompatibleProvider(
            api_key="ollama",  # Ollama ignores this, but the SDK needs a string
            base_url="http://localhost:11434/v1",
            model=os.environ.get("OLLAMA_MODEL", "llama3.2"),
        )
    raise ValueError(f"Unsupported provider: {name}")


# ---------- the chat app: depends only on Provider + neutral types ----------
class ChatApp:
    def __init__(self, provider: Provider, stream_delay: float = 0.0) -> None:
        self.provider = provider
        self.stream_delay = stream_delay
        self.history: list[Message] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.session_tokens = 0

    def reset(self) -> None:
        del self.history[1:]  # keep only the system prompt at index 0

    def run(self) -> None:
        print("Chat started. Type /reset or /exit.\n")
        try:
            while True:
                user_input = input("> ").strip()
                cmd = user_input.lower()

                if cmd == "/exit":
                    break
                if cmd == "/reset":
                    self.reset()
                    print("(history cleared)\n")
                    continue
                if not user_input:
                    continue

                self.history.append({"role": "user", "content": user_input})

                # --- display from chunks, STORE from the accumulator ---
                reply = ""
                for piece in self.provider.stream(self.history):
                    for ch in piece:  # char-by-char only for the typewriter effect
                        print(ch, end="", flush=True)
                        if self.stream_delay:
                            time.sleep(self.stream_delay)
                    reply += piece  # append once per chunk, after the char loop
                print()

                self.history.append({"role": "assistant", "content": reply})

                # --- usage + cost, all via neutral Usage ---
                usage = self.provider.last_usage()
                used = usage.total if usage else 0
                self.session_tokens += used
                print(f"[turn: {used} | session: {self.session_tokens}]")
                print(f"turn cost: ${self._cost(usage):.6f}\n")

            print("Goodbye!")
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
        except Exception as error:
            print("Error:", error)

    def _cost(self, usage: Optional[Usage]) -> float:
        if not usage:
            return 0.0
        in_price = get_float_env("INPUT_PRICE", 0.0)
        out_price = get_float_env("OUTPUT_PRICE", 0.0)
        return (usage.input_tokens / 1_000_000) * in_price \
            + (usage.output_tokens / 1_000_000) * out_price


def get_float_env(name: str, default: float = 0.0) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


if __name__ == "__main__":
    provider_name = os.environ.get("PROVIDER", "groq")
    app = ChatApp(
        make_provider(provider_name),
        stream_delay=get_float_env("STREAM_DELAY", 0.0),
    )
    app.run()