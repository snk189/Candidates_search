# Hackathon Project

## Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript (planned for later)
- **Data Storage:** JSON file (`candidates.json`)

## Project Description
A candidate registration and search system for companies. Candidates can register with their details and skills. Companies can search for candidates based on keywords and quiz them.

## Project Structure
Hackathon_project/
- backend/
  - main.py
  - models.py
  - data/
    - candidates.json
  - venv/  (not uploaded)

## Key Features
- Candidate registration
- Candidate login
- Search candidates by keywords
- Store candidate details in JSON

## How to Run Backend
1. Clone the repository.
2. Open backend folder.
3. Activate virtual environment:
   - `.\venv\Scripts\activate` (Windows PowerShell)
4. Install dependencies:
   - `pip install fastapi uvicorn`
5. Run the server:
   - `uvicorn main:app --reload`
6. Open browser or use Swagger at `http://127.0.0.1:8000/docs`
