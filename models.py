from pydantic import BaseModel
from typing import List, Optional

class CandidateIn(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    skills: List[str]

class Candidate(CandidateIn):
    quiz_score: int = 0

class Keywords(BaseModel):
    keywords: List[str]
