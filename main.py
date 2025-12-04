from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Candidate, CandidateIn, Keywords

app = FastAPI()

# CORS Enable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = [
    Candidate(name="Alice", email="alice@example.com", phone="111", password="p1", skills=["Java", "Spring"]),
    Candidate(name="David", email="david@example.com", phone="222", password="p2", skills=["Java", "React"]),
    Candidate(name="Emma", email="emma@example.com", phone="333", password="p2", skills=["Java", "React"])
]

@app.post("/register")
def register(candidate: CandidateIn):
    new_cand = Candidate(**candidate.dict())
    db.append(new_cand)
    return {"message": "Registered Successfully", "candidate": new_cand}

@app.post("/search_candidates")
def search_candidates(keywords: Keywords):
    search = [kw.lower() for kw in keywords.keywords]
    matches = []

    for cand in db:
        skills_lower = [s.lower() for s in cand.skills]
        if all(kw in skills_lower for kw in search):
            matches.append(cand)

    matches.sort(key=lambda x: x.name.lower())
    return matches
