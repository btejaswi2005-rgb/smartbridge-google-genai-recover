from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/api", tags=["Financial Health"])


@router.get("/loans/{loan_id}/financial-health", response_model=schemas.FinancialHealthOut)
def get_financial_health(loan_id: int, db: Session = Depends(get_db)):
    """
    Scenario 1 & 3: Computes EMI ratio, monthly surplus, debt stress level, and a
    recommended settlement percentage for a given loan. Deterministic and instant —
    no external API call needed, so the dashboard always has numbers to show.
    """
    loan = crud.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    borrower = crud.get_borrower(db, loan.borrower_id)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")

    return crud.compute_financial_health(borrower, loan)


@router.get("/borrowers/{borrower_id}/dashboard")
def get_dashboard(borrower_id: int, db: Session = Depends(get_db)):
    """Aggregated view for Scenario 3: every loan + its health snapshot in one call."""
    borrower = crud.get_borrower(db, borrower_id)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")

    loans = crud.get_loans_for_borrower(db, borrower_id)
    results = []
    for loan in loans:
        health = crud.compute_financial_health(borrower, loan)
        results.append({
            "loan": schemas.LoanOut.model_validate(loan).model_dump(),
            "health": health,
        })

    total_emi = sum(l.emi_amount for l in loans)
    total_outstanding = sum(l.outstanding_amount for l in loans)

    return {
        "borrower": schemas.BorrowerOut.model_validate(borrower).model_dump(),
        "loans": results,
        "summary": {
            "total_outstanding": round(total_outstanding, 2),
            "total_monthly_emi": round(total_emi, 2),
            "overall_emi_ratio": round((total_emi / borrower.monthly_income) * 100, 2)
            if borrower.monthly_income > 0 else None,
        },
    }
