import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createBorrower, createLoan } from "../api.js";

const DEMO_BORROWER_ID = 1;

export default function LoanForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    monthly_income: "",
    lender_name: "",
    loan_type: "Personal Loan",
    outstanding_amount: "",
    emi_amount: "",
    overdue_months: "0",
    interest_rate: "0",
  });
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setErrorMsg("");
    try {
      // In this prototype, a fresh borrower is created (or reused) each submit.
      // Swap for real auth/session lookup before production use.
      let borrowerId = DEMO_BORROWER_ID;
      try {
        const borrowerRes = await createBorrower({
          name: form.name,
          email: form.email,
          monthly_income: parseFloat(form.monthly_income),
        });
        borrowerId = borrowerRes.data.id;
      } catch {
        // borrower may already exist with this email in a real setup — continue with demo id
      }

      await createLoan({
        borrower_id: borrowerId,
        lender_name: form.lender_name,
        loan_type: form.loan_type,
        outstanding_amount: parseFloat(form.outstanding_amount),
        emi_amount: parseFloat(form.emi_amount),
        overdue_months: parseInt(form.overdue_months, 10),
        interest_rate: parseFloat(form.interest_rate),
      });

      navigate("/");
    } catch (err) {
      setErrorMsg("Couldn't save this loan. Check the details and try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="grid-2">
      <div className="card">
        <h2>Add a loan</h2>
        <p>Tell us about the loan and your income so we can analyze your financial health.</p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Your name</label>
            <input value={form.name} onChange={update("name")} required />
          </div>
          <div className="field">
            <label>Email</label>
            <input type="email" value={form.email} onChange={update("email")} required />
          </div>
          <div className="field">
            <label>Monthly income (₹)</label>
            <input
              type="number"
              min="0"
              value={form.monthly_income}
              onChange={update("monthly_income")}
              required
            />
          </div>
          <div className="field">
            <label>Lender name</label>
            <input value={form.lender_name} onChange={update("lender_name")} required />
          </div>
          <div className="field">
            <label>Loan type</label>
            <select value={form.loan_type} onChange={update("loan_type")}>
              <option>Personal Loan</option>
              <option>Credit Card</option>
              <option>Auto Loan</option>
              <option>Home Loan</option>
              <option>Education Loan</option>
            </select>
          </div>
          <div className="field">
            <label>Outstanding amount (₹)</label>
            <input
              type="number"
              min="0"
              value={form.outstanding_amount}
              onChange={update("outstanding_amount")}
              required
            />
          </div>
          <div className="field">
            <label>Monthly EMI (₹)</label>
            <input type="number" min="0" value={form.emi_amount} onChange={update("emi_amount")} required />
          </div>
          <div className="field">
            <label>Months overdue</label>
            <input
              type="number"
              min="0"
              value={form.overdue_months}
              onChange={update("overdue_months")}
            />
          </div>

          {errorMsg && <p style={{ color: "var(--coral)" }}>{errorMsg}</p>}

          <button className="btn btn-primary" type="submit" disabled={submitting}>
            {submitting ? "Saving…" : "Analyze my loan"}
          </button>
        </form>
      </div>

      <div className="card">
        <h3>What happens next</h3>
        <p>
          We calculate your EMI-to-income ratio, monthly surplus, and a debt-stress
          level from the numbers you enter. From there you'll get a suggested
          settlement percentage and can generate an AI negotiation letter to send
          to your lender.
        </p>
      </div>
    </div>
  );
}
