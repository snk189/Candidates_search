from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Candidate, CandidateIn, Keywords
import json
import os

app = FastAPI()

# CORS Enable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data/candidates.json"

# Ensure data folder and file exist
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Helper functions
def load_candidates():
    with open(DATA_FILE, "r") as f:
        return [Candidate(**c) for c in json.load(f)]

def save_candidates(candidates):
    with open(DATA_FILE, "w") as f:
        json.dump([c.dict() for c in candidates], f, indent=4)

# Load initial database
db = load_candidates()

@app.post("/register")
def register(candidate: CandidateIn):
    global db
    # Check for duplicate email
    for c in db:
        if c.email.lower() == candidate.email.lower():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    new_cand = Candidate(**candidate.dict())
    db.append(new_cand)
    save_candidates(db)
    return {"message": "Registered Successfully", "candidate": new_cand}

@app.post("/search_candidates")
def search_candidates(keywords: Keywords):
    search = [kw.lower() for kw in keywords.keywords]
    matches = []

    for cand in db:
        skills_lower = [s.lower() for s in cand.skills]
        if all(kw in skills_lower for kw in search):
            matches.append(cand)

    # Sort alphabetically by name
    matches.sort(key=lambda x: x.name.lower())
    return {"matching_candidates": matches}
