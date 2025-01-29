from pydantic import BaseModel

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    answer: str
