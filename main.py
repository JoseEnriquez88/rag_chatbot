from fastapi import FastAPI
from api.routes import chat

app = FastAPI(
    title="Promtior RAG Chatbot",
    description="Chatbot que responde usando el PDF de Promtior con LangChain y GPT4All.",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
