from pydantic import BaseModel
from typing import List

class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    skills: List[str]
    quiz_score: int = 0
