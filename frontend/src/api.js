import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

// Borrowers
export const createBorrower = (data) => api.post("/borrowers", data);
export const getBorrower = (id) => api.get(`/borrowers/${id}`);
export const getDashboard = (borrowerId) => api.get(`/borrowers/${borrowerId}/dashboard`);

// Loans
export const createLoan = (data) => api.post("/loans", data);
export const getLoansForBorrower = (borrowerId) => api.get(`/borrowers/${borrowerId}/loans`);
export const deleteLoan = (loanId) => api.delete(`/loans/${loanId}`);

// Financial health
export const getFinancialHealth = (loanId) => api.get(`/loans/${loanId}/financial-health`);

// Negotiation
export const generateNegotiation = (loanId, tone) =>
  api.post("/negotiation/generate", { loan_id: loanId, tone });
export const getNegotiationHistory = (loanId) => api.get(`/loans/${loanId}/negotiation-history`);

export default api;
