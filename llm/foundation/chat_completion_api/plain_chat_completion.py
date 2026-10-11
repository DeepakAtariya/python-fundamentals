import os

from dotenv import load_dotenv  # type: ignore
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam

load_dotenv()

# Point the OpenAI SDK at Groq — same SDK, different base_url
client: OpenAI = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_MSG: ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": "You are a helpful assistant and this is a CUI based interface. Please limit the output to 50 words.",
}


def clear_chat(history: list[ChatCompletionMessageParam]) -> None:
    del history[1:]  # keep only the system prompt at index 0


def main() -> None:
    chat_history: list[ChatCompletionMessageParam] = [SYSTEM_MSG]
    session_tokens: int = 0

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
            )

            reply: str = response.choices[0].message.content or ""
            chat_history.append({"role": "assistant", "content": reply})

            usage = response.usage
            used: int = usage.total_tokens if usage else 0
            session_tokens += used
            input_price = float(os.getenv("INPUT_PRICE", "0"))
            output_price = float(os.getenv("OUTPUT_PRICE", "0"))
            turn_cost: float = (
                (usage.prompt_tokens / 1_000_000) * input_price
                + (usage.completion_tokens / 1_000_000) * output_price
                if usage
                else 0.0
            )
            print(f"\n{reply}\n[turn: {used} | session: {session_tokens}]\n")
            print(f"Turn cost: ${turn_cost:.6f}\n")

        print("Goodbye!")

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
    except Exception as error:
        print("Error: ", error)


if __name__ == "__main__":
    main()