from typing import List
from pydantic import BaseModel

class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    skills: List[str]
    quiz_score: int = 0

class KeywordSearch(BaseModel):
    keywords: List[str]
