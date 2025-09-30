import os
from keys import GEMINI_KEYS

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = GEMINI_KEYS[2]

from langchain.chat_models import init_chat_model
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

gemini = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai",
    temperature=0.0
)

gemini_embedding = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    task_type="retrieval_document",
)
