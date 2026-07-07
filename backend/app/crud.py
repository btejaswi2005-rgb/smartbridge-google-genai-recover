from sqlalchemy.orm import Session
from . import models, schemas


# ---------- Borrower ----------
def create_borrower(db: Session, borrower: schemas.BorrowerCreate) -> models.Borrower:
    db_borrower = models.Borrower(**borrower.model_dump())
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    return db_borrower


def get_borrower(db: Session, borrower_id: int) -> models.Borrower | None:
    return db.query(models.Borrower).filter(models.Borrower.id == borrower_id).first()


# ---------- Loan ----------
def create_loan(db: Session, loan: schemas.LoanCreate) -> models.Loan:
    db_loan = models.Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_loan(db: Session, loan_id: int) -> models.Loan | None:
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()


def get_loans_for_borrower(db: Session, borrower_id: int) -> list[models.Loan]:
    return db.query(models.Loan).filter(models.Loan.borrower_id == borrower_id).all()


def delete_loan(db: Session, loan_id: int) -> bool:
    loan = get_loan(db, loan_id)
    if not loan:
        return False
    db.delete(loan)
    db.commit()
    return True


# ---------- Negotiation history ----------
def save_negotiation_record(
    db: Session,
    loan_id: int,
    strategy_type: str,
    generated_content: str,
    settlement_percentage: float | None,
    debt_stress_level: str | None,
) -> models.NegotiationRecord:
    record = models.NegotiationRecord(
        loan_id=loan_id,
        strategy_type=strategy_type,
        generated_content=generated_content,
        settlement_percentage=settlement_percentage,
        debt_stress_level=debt_stress_level,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_negotiation_history(db: Session, loan_id: int) -> list[models.NegotiationRecord]:
    return (
        db.query(models.NegotiationRecord)
        .filter(models.NegotiationRecord.loan_id == loan_id)
        .order_by(models.NegotiationRecord.created_at.desc())
        .all()
    )


# ---------- Financial health engine (deterministic, rule-based) ----------
def compute_financial_health(borrower: models.Borrower, loan: models.Loan) -> dict:
    """
    Rule-based debt-stress and settlement engine. This runs independently of the
    Gemini API so the app always has a numeric baseline, even if the AI call fails
    or is used only for the narrative/letter layer on top of these numbers.
    """
    income = borrower.monthly_income
    emi = loan.emi_amount

    emi_ratio = round((emi / income) * 100, 2) if income > 0 else 100.0
    monthly_surplus = round(income - emi, 2)

    # Debt stress banding based on EMI-to-income ratio + overdue history
    if emi_ratio < 30 and loan.overdue_months == 0:
        stress_level = "Low"
        base_settlement_pct = 0.0
    elif emi_ratio < 45 and loan.overdue_months <= 2:
        stress_level = "Moderate"
        base_settlement_pct = 15.0
    elif emi_ratio < 60 or loan.overdue_months <= 5:
        stress_level = "High"
        base_settlement_pct = 30.0
    else:
        stress_level = "Severe"
        base_settlement_pct = 45.0

    # Overdue months push the settlement ask higher (lender more willing to negotiate)
    overdue_adjustment = min(loan.overdue_months * 2, 20)
    settlement_pct = min(base_settlement_pct + overdue_adjustment, 60.0)
    settlement_amount = round(loan.outstanding_amount * (1 - settlement_pct / 100), 2)

    insights = {
        "Low": "Your EMI load is manageable relative to income. Focus on steady repayment rather than settlement.",
        "Moderate": "EMI burden is becoming noticeable. A partial settlement or restructuring conversation is worth starting now.",
        "High": "Your debt load is significantly straining monthly income. Prioritize a settlement negotiation with this lender.",
        "Severe": "This loan is in critical distress. Immediate settlement negotiation or restructuring is strongly recommended.",
    }

    return {
        "loan_id": loan.id,
        "monthly_income": income,
        "emi_amount": emi,
        "emi_ratio": emi_ratio,
        "monthly_surplus": monthly_surplus,
        "overdue_months": loan.overdue_months,
        "debt_stress_level": stress_level,
        "recommended_settlement_percentage": settlement_pct,
        "settlement_amount": settlement_amount,
        "insight": insights[stress_level],
    }
