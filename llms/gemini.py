import os

from keys import GEMINI_KEYS

from langchain.chat_models import init_chat_model

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = GEMINI_KEYS[0]

gemini = init_chat_model("gemini-2.5-flash", model_provider="google_genai")