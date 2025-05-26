from fastapi import APIRouter
from pydantic import BaseModel
from core.rag_chain import ask_question

router = APIRouter()

class QueryInput(BaseModel):
    query: str

@router.post("/")
async def ask(input: QueryInput):
    try:
        answer = ask_question(input.query)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
