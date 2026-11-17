"""Live smoke test: python test_smoke.py  (needs GROQ_API_KEY)."""
from groq_client import DEFAULT_MODEL, get_client

resp = get_client().chat.completions.create(
    model=DEFAULT_MODEL,
    messages=[{"role": "user", "content": "Reply with exactly: pong"}],
    max_tokens=200,
    temperature=0,
)
text = resp.choices[0].message.content.strip()
print(f"{DEFAULT_MODEL}: {text!r}")
assert "pong" in text.lower(), "unexpected reply"
print("OK")
