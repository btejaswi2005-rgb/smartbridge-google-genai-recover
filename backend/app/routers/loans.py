from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/api", tags=["Loans & Borrowers"])


@router.post("/borrowers", response_model=schemas.BorrowerOut)
def create_borrower(borrower: schemas.BorrowerCreate, db: Session = Depends(get_db)):
    return crud.create_borrower(db, borrower)


@router.get("/borrowers/{borrower_id}", response_model=schemas.BorrowerOut)
def read_borrower(borrower_id: int, db: Session = Depends(get_db)):
    borrower = crud.get_borrower(db, borrower_id)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return borrower


@router.post("/loans", response_model=schemas.LoanOut)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    borrower = crud.get_borrower(db, loan.borrower_id)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return crud.create_loan(db, loan)


@router.get("/loans/{loan_id}", response_model=schemas.LoanOut)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.get("/borrowers/{borrower_id}/loans", response_model=list[schemas.LoanOut])
def read_loans_for_borrower(borrower_id: int, db: Session = Depends(get_db)):
    return crud.get_loans_for_borrower(db, borrower_id)


@router.delete("/loans/{loan_id}")
def remove_loan(loan_id: int, db: Session = Depends(get_db)):
    if not crud.delete_loan(db, loan_id):
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"detail": "Loan deleted"}
