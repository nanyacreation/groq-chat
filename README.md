# Groq Chat

A free AI chat powered by [Groq](https://console.groq.com)'s OpenAI-compatible API:
a password-protected **web app** (Streamlit) plus small **terminal scripts**.

## Deploy live (Streamlit Community Cloud, free)

1. Go to https://share.streamlit.io and sign in with GitHub.
2. **Create app** → *Deploy a public app from GitHub* → pick this repo,
   branch `main`, main file `app.py`.
3. Open **Advanced settings → Secrets** and paste:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   APP_PASSWORD = "choose-a-strong-password"
   ```
4. **Deploy**. You get a URL like `https://<name>.streamlit.app`.
   Share it plus the password only with people you trust — they use your Groq quota.

Change secrets later in the app's **⋮ → Settings → Secrets**. Every push to
`main` redeploys automatically.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add GROQ_API_KEY and APP_PASSWORD
streamlit run app.py        # web app at http://localhost:8501
python chat.py              # terminal chat
python models.py            # list models available to your key
python test_smoke.py        # live check that key + model work
```

## Files

| File | Purpose |
|---|---|
| `app.py` | Web chat with password gate, model picker, system prompt |
| `chat.py` | Terminal chat (interactive or one-shot) |
| `groq_client.py` | Shared client setup for the scripts |
| `models.py`, `test_smoke.py` | Model list and live smoke test |

Never commit `.env` or `.streamlit/secrets.toml` (both are git-ignored).
Free-tier rate limits apply; a `429` error means wait and retry.
