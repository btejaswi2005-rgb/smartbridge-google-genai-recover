from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ---------- Borrower ----------
class BorrowerCreate(BaseModel):
    name: str
    email: EmailStr
    monthly_income: float


class BorrowerOut(BorrowerCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Loan ----------
class LoanCreate(BaseModel):
    borrower_id: int
    lender_name: str
    loan_type: str = "Personal Loan"
    outstanding_amount: float
    emi_amount: float
    overdue_months: int = 0
    interest_rate: float = 0.0


class LoanOut(LoanCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Financial Health ----------
class FinancialHealthOut(BaseModel):
    loan_id: int
    monthly_income: float
    emi_amount: float
    emi_ratio: float           # emi / income, %
    monthly_surplus: float     # income - emi
    overdue_months: int
    debt_stress_level: str     # Low | Moderate | High | Severe
    recommended_settlement_percentage: float
    settlement_amount: float
    insight: str


# ---------- Negotiation ----------
class NegotiationRequest(BaseModel):
    loan_id: int
    tone: str = "professional"  # professional | firm | empathetic


class NegotiationOut(BaseModel):
    id: int
    loan_id: int
    strategy_type: str
    settlement_percentage: Optional[float]
    generated_content: str
    debt_stress_level: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
