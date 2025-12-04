from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Candidate
import json
import os
from typing import List

app = FastAPI()

CANDIDATE_FILE = "data/candidates.json"

# Ensure data folder and file exist
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(CANDIDATE_FILE):
    with open(CANDIDATE_FILE, "w") as f:
        json.dump([], f)

# ----- Pydantic models for requests -----
class RegisterRequest(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    skills: List[str]

class LoginRequest(BaseModel):
    email: str
    password: str

class KeywordRequest(BaseModel):
    keywords: List[str]

# ----- API Endpoints -----

@app.post("/register")
def register_candidate(request: RegisterRequest):
    with open(CANDIDATE_FILE, "r") as f:
        candidates = json.load(f)

    # Check if email already exists
    if any(c["email"] == request.email for c in candidates):
        raise HTTPException(status_code=400, detail="Email already registered")

    candidate = Candidate(**request.dict())
    candidates.append(candidate.dict())

    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=4)

    return {"message": "Candidate registered successfully"}


@app.post("/login")
def login_candidate(request: LoginRequest):
    with open(CANDIDATE_FILE, "r") as f:
        candidates = json.load(f)

    for c in candidates:
        if c["email"] == request.email and c["password"] == request.password:
            return {"message": "Login successful", "candidate": c}

    raise HTTPException(status_code=400, detail="Invalid email or password")


@app.post("/search_candidates")
def search_candidates(request: KeywordRequest):
    with open(CANDIDATE_FILE, "r") as f:
        candidates = json.load(f)

    results = []
    for c in candidates:
        if any(skill in c["skills"] for skill in request.keywords):
            results.append(c)

    return {"candidates": results}
