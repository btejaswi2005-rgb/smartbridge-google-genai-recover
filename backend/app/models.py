from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    monthly_income = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    loans = relationship("Loan", back_populates="borrower", cascade="all, delete-orphan")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)

    lender_name = Column(String, nullable=False)
    loan_type = Column(String, default="Personal Loan")
    outstanding_amount = Column(Float, nullable=False)
    emi_amount = Column(Float, nullable=False)
    overdue_months = Column(Integer, default=0)
    interest_rate = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)

    borrower = relationship("Borrower", back_populates="loans")
    negotiations = relationship("NegotiationRecord", back_populates="loan", cascade="all, delete-orphan")


class NegotiationRecord(Base):
    """Stores every AI-generated negotiation letter / settlement strategy for history tracking."""

    __tablename__ = "negotiation_records"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)

    strategy_type = Column(String, default="settlement_letter")  # settlement_letter | recommendation
    settlement_percentage = Column(Float, nullable=True)
    generated_content = Column(Text, nullable=False)
    debt_stress_level = Column(String, nullable=True)  # Low | Moderate | High | Severe

    created_at = Column(DateTime, default=datetime.utcnow)

    loan = relationship("Loan", back_populates="negotiations")
