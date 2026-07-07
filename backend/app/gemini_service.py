import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

_model = None


def _get_model():
    """Lazily configure and cache the Gemini model client."""
    global _model
    if _model is None:
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to backend/.env before calling AI features."
            )
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model


TONE_GUIDANCE = {
    "professional": "formal, businesslike, and neutral in tone",
    "firm": "polite but firm, making clear the borrower has limited capacity to pay more",
    "empathetic": "warm and cooperative, emphasizing good-faith intent to resolve the debt",
}


def build_negotiation_prompt(borrower_name: str, lender_name: str, loan_type: str,
                              outstanding_amount: float, emi_amount: float,
                              overdue_months: int, monthly_income: float,
                              health: dict, tone: str) -> str:
    """
    Prompt-engineered template: grounds the model in real borrower numbers so the
    letter is specific and defensible rather than a generic template, and constrains
    format/length so output is directly usable.
    """
    tone_desc = TONE_GUIDANCE.get(tone, TONE_GUIDANCE["professional"])

    return f"""You are a financial correspondence assistant helping a borrower communicate with a lender.
Write a {tone_desc} settlement negotiation letter/email from the borrower to the lender.

BORROWER: {borrower_name}
LENDER: {lender_name}
LOAN TYPE: {loan_type}
OUTSTANDING AMOUNT: {outstanding_amount}
CURRENT EMI: {emi_amount}
MONTHS OVERDUE: {overdue_months}
MONTHLY INCOME: {monthly_income}
DEBT STRESS LEVEL: {health['debt_stress_level']}
SUGGESTED SETTLEMENT OFFER: {health['recommended_settlement_percentage']}% off outstanding amount
(i.e. approximately {health['settlement_amount']} as a one-time settlement figure)

Requirements:
- Address it to the lender's collections/recovery department.
- State the borrower's genuine financial hardship briefly and factually, without exaggeration.
- Propose the settlement figure above as an opening negotiation position, and note openness to reasonable counter-offers.
- Keep it under 250 words.
- End with a professional closing and a placeholder signature line.
- Do not invent specific dates, account numbers, or legal claims not provided above.
- Output only the letter text, no preamble or explanation."""


def generate_negotiation_letter(borrower_name: str, lender_name: str, loan_type: str,
                                  outstanding_amount: float, emi_amount: float,
                                  overdue_months: int, monthly_income: float,
                                  health: dict, tone: str = "professional") -> str:
    """Scenario 2: Gemini-generated lender-specific negotiation letter."""
    model = _get_model()
    prompt = build_negotiation_prompt(
        borrower_name, lender_name, loan_type, outstanding_amount, emi_amount,
        overdue_months, monthly_income, health, tone,
    )
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_settlement_narrative(health: dict) -> str:
    """
    Scenario 1: a short AI narrative layered on top of the deterministic settlement
    numbers from crud.compute_financial_health, to explain *why* in plain language.
    """
    model = _get_model()
    prompt = f"""A borrower has the following financial snapshot:
- EMI-to-income ratio: {health['emi_ratio']}%
- Monthly surplus after EMI: {health['monthly_surplus']}
- Months overdue: {health['overdue_months']}
- Debt stress level: {health['debt_stress_level']}
- Suggested settlement offer: {health['recommended_settlement_percentage']}%

In 3-4 short sentences, explain this financial situation in plain, encouraging,
non-judgmental language a stressed borrower could easily understand, and explain
why this settlement percentage is a reasonable opening position. Output only the
explanation text."""
    response = model.generate_content(prompt)
    return response.text.strip()
