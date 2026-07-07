from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import loans, financial_health, negotiation

# Create tables on startup (fine for SQLite + a dev/prototype project;
# swap for Alembic migrations if this grows into production use)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Debt Relief & Financial Recovery Platform",
    description="APIs for loan management, financial health analysis, and AI-assisted negotiation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loans.router)
app.include_router(financial_health.router)
app.include_router(negotiation.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "debt-relief-platform-api"}
