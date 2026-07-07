# Recover — AI-Powered Debt Relief & Financial Recovery Platform

An AI-powered platform that helps borrowers manage loans, understand their debt
stress, and generate lender-specific negotiation letters using Google Gemini.

## Stack
- **Frontend:** React.js (Vite) + React Router + Axios
- **Backend:** FastAPI + SQLAlchemy ORM + SQLite
- **AI:** Google Gemini API (`gemini-1.5-flash`)

## Project structure
```
smart-bridge/
  backend/
    app/
      main.py            FastAPI app + CORS + routers
      database.py         SQLAlchemy engine/session
      models.py            Borrower, Loan, NegotiationRecord
      schemas.py           Pydantic request/response models
      crud.py              DB operations + financial-health engine
      gemini_service.py   Gemini prompt building + calls
      routers/
        loans.py
        financial_health.py
        negotiation.py
    requirements.txt
    .env.example
  frontend/
    src/
      pages/               Dashboard, LoanForm, NegotiationLetter
      components/          Navbar, LoanCard, RecoveryPath
      api.js               Axios client
      index.css            Design tokens + styles
    package.json
```

## Setup

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and add your real Gemini API key:
# GEMINI_API_KEY=your_actual_key_here
# Get a key at https://aistudio.google.com/app/apikey

uvicorn app.main:app --reload --port 8000
```
Backend runs at `http://localhost:8000`. Interactive API docs at
`http://localhost:8000/docs`.

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

## How the three scenarios map to the code

**Scenario 1 — AI-powered settlement recommendation**
`POST /api/loans` saves the loan → `GET /api/loans/{id}/financial-health`
(`crud.compute_financial_health`) computes EMI ratio, monthly surplus, debt
stress level, and a recommended settlement percentage. This is deterministic
rule-based logic, so the dashboard always has numbers even before any AI call.

**Scenario 2 — Intelligent negotiation letter generation**
`POST /api/negotiation/generate` (`gemini_service.generate_negotiation_letter`)
sends the loan's real numbers and computed stress level to Gemini with a
tone-controlled prompt, and stores the result via
`crud.save_negotiation_record` for history.

**Scenario 3 — Financial health tracking & loan analysis**
`GET /api/borrowers/{id}/dashboard` aggregates every loan + its health snapshot,
and `GET /api/loans/{id}/negotiation-history` returns past AI-generated letters
so the borrower can track their negotiation attempts over time.

## Notes for continuing this project
- Auth is stubbed with a single demo borrower ID (`DEMO_BORROWER_ID = 1` in the
  frontend) — swap in real login/session handling before treating this as
  production-ready.
- The negotiation letter route will return a 503 with a clear message if
  `GEMINI_API_KEY` isn't set — check `backend/.env` first if that happens.
- SQLite is used for simplicity (`debt_relief.db` is created automatically on
  first run); swap `DATABASE_URL` in `.env` for Postgres/MySQL if you need
  multi-user concurrency.
