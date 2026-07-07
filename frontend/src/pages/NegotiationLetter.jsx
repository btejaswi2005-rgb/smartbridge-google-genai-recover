import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { generateNegotiation, getNegotiationHistory } from "../api.js";

export default function NegotiationLetter() {
  const [searchParams] = useSearchParams();
  const loanIdParam = searchParams.get("loanId");

  const [loanId, setLoanId] = useState(loanIdParam || "");
  const [tone, setTone] = useState("professional");
  const [letter, setLetter] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const loadHistory = (id) => {
    getNegotiationHistory(id)
      .then((res) => setHistory(res.data))
      .catch(() => setHistory([]));
  };

  useEffect(() => {
    if (loanIdParam) loadHistory(loanIdParam);
  }, [loanIdParam]);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");
    setLetter(null);
    try {
      const res = await generateNegotiation(parseInt(loanId, 10), tone);
      setLetter(res.data);
      loadHistory(loanId);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setErrorMsg(
        detail || "Couldn't generate a letter right now. Check the loan ID and your Gemini API key."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid-2">
      <div className="card">
        <h2>Generate a negotiation letter</h2>
        <p>Gemini drafts a settlement letter grounded in this loan's real numbers.</p>

        <form onSubmit={handleGenerate}>
          <div className="field">
            <label>Loan ID</label>
            <input value={loanId} onChange={(e) => setLoanId(e.target.value)} required />
          </div>
          <div className="field">
            <label>Tone</label>
            <select value={tone} onChange={(e) => setTone(e.target.value)}>
              <option value="professional">Professional</option>
              <option value="firm">Firm</option>
              <option value="empathetic">Empathetic</option>
            </select>
          </div>
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Drafting…" : "Generate letter"}
          </button>
        </form>

        {errorMsg && (
          <p style={{ color: "var(--coral)", marginTop: 16 }}>{errorMsg}</p>
        )}

        {letter && (
          <div style={{ marginTop: 24 }}>
            <h3>Your draft</h3>
            <div className="letter-box">{letter.generated_content}</div>
          </div>
        )}
      </div>

      <div className="card">
        <h3>Negotiation history</h3>
        {history.length === 0 ? (
          <p>No letters generated yet for this loan.</p>
        ) : (
          history.map((h) => (
            <div key={h.id} style={{ borderBottom: "1px solid var(--line)", padding: "12px 0" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span className={`stress-badge stress-${h.debt_stress_level}`}>
                  {h.debt_stress_level}
                </span>
                <span className="mono" style={{ fontSize: 12, color: "var(--slate)" }}>
                  {new Date(h.created_at).toLocaleDateString()}
                </span>
              </div>
              <p style={{ fontSize: 13, marginTop: 6 }}>
                Settlement offer: {h.settlement_percentage}%
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
