from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

DATA_FILE = "data/candidates.json"

class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    skills: List[str]

class LoginData(BaseModel):
    email: str
    password: str

class Keywords(BaseModel):
    keywords: List[str]

# Helper to read candidates safely
def read_candidates():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    except json.JSONDecodeError:
        return []

# Helper to write candidates
def write_candidates(candidates):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(candidates, f, indent=4)

@app.post("/register")
def register(candidate: Candidate):
    candidates = read_candidates()
    if any(c["email"] == candidate.email for c in candidates):
        raise HTTPException(status_code=400, detail="Email already registered")
    c_dict = candidate.dict()
    c_dict["quiz_score"] = 0  # always initialize to 0
    candidates.append(c_dict)
    write_candidates(candidates)
    return {"message": "Candidate registered successfully"}

@app.post("/login")
def login(data: LoginData):
    candidates = read_candidates()
    for c in candidates:
        if c["email"] == data.email and c["password"] == data.password:
            return {"message": "Login successful", "candidate": c}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/search_candidates")
def search_candidates(keywords: Keywords):
    candidates = read_candidates()
    matched = []
    for c in candidates:
        match_count = sum(1 for k in keywords.keywords if k in c.get("skills", []))
        if match_count > 0:
            matched.append((match_count, c["name"].lower(), c))
    # Sort by number of matches descending, then alphabetically by name
    matched.sort(key=lambda x: (-x[0], x[1]))
    return {"matching_candidates": [c[2] for c in matched]}
