from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
USER_NAME = os.getenv("USER_NAME")
DOCUMENT_LANGUAGES = os.getenv("DOCUMENT_LANGUAGES")

origins = [
    "http://localhost:3000",
]
