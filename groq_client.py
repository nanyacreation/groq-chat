"""Shared Groq client (OpenAI-compatible API)."""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def get_client() -> OpenAI:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise SystemExit("GROQ_API_KEY is not set. Copy .env.example to .env and add your key.")
    return OpenAI(base_url=BASE_URL, api_key=key)
