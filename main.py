from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from models import Candidate

app = FastAPI()

DATA_FILE = "data/candidates.json"

class CandidateIn(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    skills: List[str]

class Keywords(BaseModel):
    keywords: List[str]

def load_candidates():
    with open(DATA_FILE, "r") as f:
        return [Candidate(**cand) for cand in json.load(f)]

def save_candidates(candidates):
    with open(DATA_FILE, "w") as f:
        json.dump([cand.dict() for cand in candidates], f, indent=4)

@app.post("/register")
def register_candidate(candidate: CandidateIn):
    candidates = load_candidates()
    if any(c.email == candidate.email for c in candidates):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_candidate = Candidate(**candidate.dict(), quiz_score=0)
    candidates.append(new_candidate)
    save_candidates(candidates)
    return {"message": "Candidate registered successfully"}

@app.post("/login")
def login(email: str, password: str):
    candidates = load_candidates()
    for c in candidates:
        if c.email == email and c.password == password:
            return {"message": "Login successful", "candidate": c.dict()}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/search_candidates")
def search_candidates(keywords: Keywords):
    candidates = load_candidates()
    result = []

    for cand in candidates:
        match_count = len(set(cand.skills) & set(keywords.keywords))
        if match_count > 0:
            result.append((match_count, cand.name.lower(), cand))  # add name for alphabetical sort

    # Sort first by match_count descending, then name ascending
    result.sort(key=lambda x: (-x[0], x[1]))

    return {"matching_candidates": [cand[2].dict() for cand in result]}
