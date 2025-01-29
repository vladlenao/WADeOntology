from fastapi import APIRouter
from .services import QAService
from .models import Question

router = APIRouter(prefix="/qa", tags=["Question-Answering"])

@router.post("/ask")
def ask_question(question: Question):
    answer = QAService.answer_question(question.text)
    return {"answer": answer.answer}
