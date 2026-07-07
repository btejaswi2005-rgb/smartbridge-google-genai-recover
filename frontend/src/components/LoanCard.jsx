import { Link } from "react-router-dom";
import RecoveryPath from "./RecoveryPath.jsx";

export default function LoanCard({ loan, health }) {
  return (
    <div className="card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <h3>{loan.lender_name}</h3>
        <span className={`stress-badge stress-${health.debt_stress_level}`}>
          {health.debt_stress_level} stress
        </span>
      </div>
      <p style={{ marginTop: 4 }}>{loan.loan_type}</p>

      <RecoveryPath stressLevel={health.debt_stress_level} />

      <div className="metrics-row">
        <div>
          <div className="metric-label">Outstanding</div>
          <div className="metric-value">₹{loan.outstanding_amount.toLocaleString()}</div>
        </div>
        <div>
          <div className="metric-label">EMI ratio</div>
          <div className="metric-value">{health.emi_ratio}%</div>
        </div>
        <div>
          <div className="metric-label">Monthly surplus</div>
          <div className="metric-value">₹{health.monthly_surplus.toLocaleString()}</div>
        </div>
        <div>
          <div className="metric-label">Suggested offer</div>
          <div className="metric-value">{health.recommended_settlement_percentage}%</div>
        </div>
      </div>

      <p style={{ fontSize: 13 }}>{health.insight}</p>

      <Link to={`/negotiate?loanId=${loan.id}`} className="btn btn-primary" style={{ textDecoration: "none" }}>
        Generate negotiation letter
      </Link>
    </div>
  );
}
