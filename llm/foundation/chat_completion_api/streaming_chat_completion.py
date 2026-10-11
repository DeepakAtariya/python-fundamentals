import os
import time
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from openai.types import CompletionUsage
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
)

load_dotenv()

# Point the OpenAI SDK at Groq — same SDK, different base_url
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_MSG: ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": "You are a helpful assistant and this is a CUI based interface. Please limit the output to 50 words.",
}


def clear_chat(history: list[ChatCompletionMessageParam]) -> None:
    if len(history) > 1:
        del history[1:]  # keep only the system prompt at index 0


def get_float_env(name: str, default: float = 0.0) -> float:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


def main() -> None:
    chat_history: list[ChatCompletionMessageParam] = [SYSTEM_MSG]
    session_tokens = 0

    print("Chat started. Type /reset or /exit.\n")

    try:
        while True:
            user_question = input("> ").strip()
            cmd = user_question.lower()

            # --- commands are checked BEFORE anything is sent or stored ---
            if cmd == "/exit":
                break

            if cmd == "/reset":
                clear_chat(chat_history)
                print("(history cleared)\n")
                continue

            if not user_question:
                continue  # ignore empty input

            # --- only real messages reach the history and the API ---
            chat_history.append({"role": "user", "content": user_question})

            response = client.chat.completions.create(
                model=os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b"),
                messages=chat_history,
                stream=True,
                stream_options={"include_usage": True},
            )
            stream_delay = get_float_env("STREAM_DELAY", 0.02)
            reply = ""
            usage: Optional[CompletionUsage] = None
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    for ch in content:
                        print(ch, end="", flush=True)
                        time.sleep(stream_delay)
                    reply += content
                if chunk.usage:
                    usage = chunk.usage

            chat_history.append({"role": "assistant", "content": reply})

            used = usage.total_tokens if usage else 0
            session_tokens += used
            print(f"\n[turn: {used} | session: {session_tokens}]\n")

            input_price = get_float_env("INPUT_PRICE")
            output_price = get_float_env("OUTPUT_PRICE")
            turn_cost: float = 0.0
            if usage:
                turn_cost = (
                    (usage.prompt_tokens / 1_000_000) * input_price
                    + (usage.completion_tokens / 1_000_000) * output_price
                )

            print(f"Turn cost: ${turn_cost:.6f}\n")

        print("Goodbye!")

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
    except Exception as error:
        print("Error: ", error)


if __name__ == "__main__":
    main()