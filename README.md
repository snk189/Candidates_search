# Candidate Search Platform

## Overview
FastAPI backend + HTML/CSS frontend to register candidates and search by skills. Data is stored in `data/candidates.json`.

## Tech Stack
- Backend: FastAPI, Python  
- Frontend: HTML, CSS, JS  
- Storage: JSON file  

## Features
- Register candidates (name, email, phone, password, skills, quiz_score=0)  
- Search candidates by skill keywords (case-insensitive, alphabetically sorted)  
- Persistent storage in JSON  

## Setup
1. Create virtual env & install dependencies:
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn pydantic
Run backend:

Copy code
uvicorn main:app --reload
API docs: http://127.0.0.1:8000/docs

API Endpoints
POST /register – Register candidate

POST /search_candidates – Search by skills

Notes<br>
Ensure data/candidates.json exists.<br>
Frontend connects to FastAPI endpoints.

