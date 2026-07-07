import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import LoanForm from "./pages/LoanForm.jsx";
import NegotiationLetter from "./pages/NegotiationLetter.jsx";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/add-loan" element={<LoanForm />} />
        <Route path="/negotiate" element={<NegotiationLetter />} />
      </Routes>
    </div>
  );
}
