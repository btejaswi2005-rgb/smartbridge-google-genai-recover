from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, gemini_service
from ..database import get_db

router = APIRouter(prefix="/api", tags=["Negotiation"])


@router.post("/negotiation/generate", response_model=schemas.NegotiationOut)
def generate_negotiation(request: schemas.NegotiationRequest, db: Session = Depends(get_db)):
    """
    Scenario 2: Uses Gemini to draft a lender-specific settlement negotiation letter,
    grounded in the loan's real numbers and its computed debt-stress profile, then
    stores the result in negotiation history.
    """
    loan = crud.get_loan(db, request.loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    borrower = crud.get_borrower(db, loan.borrower_id)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")

    health = crud.compute_financial_health(borrower, loan)

    try:
        letter = gemini_service.generate_negotiation_letter(
            borrower_name=borrower.name,
            lender_name=loan.lender_name,
            loan_type=loan.loan_type,
            outstanding_amount=loan.outstanding_amount,
            emi_amount=loan.emi_amount,
            overdue_months=loan.overdue_months,
            monthly_income=borrower.monthly_income,
            health=health,
            tone=request.tone,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    record = crud.save_negotiation_record(
        db,
        loan_id=loan.id,
        strategy_type="settlement_letter",
        generated_content=letter,
        settlement_percentage=health["recommended_settlement_percentage"],
        debt_stress_level=health["debt_stress_level"],
    )
    return record


@router.get("/loans/{loan_id}/negotiation-history", response_model=list[schemas.NegotiationOut])
def negotiation_history(loan_id: int, db: Session = Depends(get_db)):
    """Scenario 3: AI-generated negotiation history for a loan."""
    loan = crud.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return crud.get_negotiation_history(db, loan_id)
