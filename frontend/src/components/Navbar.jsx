import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar">
      <div className="brand">
        <div className="brand-mark">R</div>
        <span className="brand-name">Recover</span>
      </div>
      <div className="nav-links">
        <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
          Dashboard
        </NavLink>
        <NavLink to="/add-loan" className={({ isActive }) => (isActive ? "active" : "")}>
          Add loan
        </NavLink>
        <NavLink to="/negotiate" className={({ isActive }) => (isActive ? "active" : "")}>
          Negotiate
        </NavLink>
      </div>
    </div>
  );
}
