import os

from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BACKEND_JWT_TOKEN = os.getenv("BACKEND_JWT_TOKEN")

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8080",
).rstrip("/")


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )

if not BACKEND_JWT_TOKEN:
    raise ValueError(
        "BACKEND_JWT_TOKEN is missing. Add it to your .env file."
    )