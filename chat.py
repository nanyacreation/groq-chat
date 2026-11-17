"""Interactive streaming chat with a Groq model.

Usage:
    python chat.py                 # interactive chat
    python chat.py "your prompt"   # one-shot answer
"""
import sys

from groq_client import DEFAULT_MODEL, get_client


def stream_reply(client, messages, model=DEFAULT_MODEL) -> str:
    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    parts = []
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
        parts.append(delta)
    print()
    return "".join(parts)


def main() -> None:
    client = get_client()
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    if len(sys.argv) > 1:
        messages.append({"role": "user", "content": " ".join(sys.argv[1:])})
        stream_reply(client, messages)
        return

    print(f"Chatting with {DEFAULT_MODEL}. Ctrl+C or 'exit' to quit.")
    while True:
        try:
            user = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user.lower() in {"exit", "quit"}:
            break
        if not user:
            continue
        messages.append({"role": "user", "content": user})
        print("ai> ", end="")
        messages.append({"role": "assistant", "content": stream_reply(client, messages)})


if __name__ == "__main__":
    main()
