import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getDashboard } from "../api.js";
import LoanCard from "../components/LoanCard.jsx";

// Prototype-stage: a single borrower ID stands in for real auth/session handling.
const DEMO_BORROWER_ID = 1;

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getDashboard(DEMO_BORROWER_ID)
      .then((res) => setData(res.data))
      .catch(() => setError("no-borrower"));
  }, []);

  if (error) {
    return (
      <div className="empty-state">
        <h2>No borrower profile yet</h2>
        <p>Add your first loan to create a profile and see your financial health.</p>
        <Link to="/add-loan" className="btn btn-primary" style={{ textDecoration: "none" }}>
          Add your first loan
        </Link>
      </div>
    );
  }

  if (!data) return <p>Loading your financial picture…</p>;

  const { borrower, loans, summary } = data;

  return (
    <div>
      <h1>Welcome back, {borrower.name.split(" ")[0]}</h1>
      <p>Here's where your debt recovery stands today.</p>

      <div className="metrics-row" style={{ marginBottom: 32 }}>
        <div className="card">
          <div className="metric-label">Total outstanding</div>
          <div className="metric-value">₹{summary.total_outstanding.toLocaleString()}</div>
        </div>
        <div className="card">
          <div className="metric-label">Total monthly EMI</div>
          <div className="metric-value">₹{summary.total_monthly_emi.toLocaleString()}</div>
        </div>
        <div className="card">
          <div className="metric-label">Overall EMI ratio</div>
          <div className="metric-value">{summary.overall_emi_ratio}%</div>
        </div>
      </div>

      {loans.length === 0 ? (
        <div className="empty-state">
          <p>No loans added yet.</p>
          <Link to="/add-loan" className="btn btn-primary" style={{ textDecoration: "none" }}>
            Add a loan
          </Link>
        </div>
      ) : (
        loans.map(({ loan, health }) => <LoanCard key={loan.id} loan={loan} health={health} />)
      )}
    </div>
  );
}
