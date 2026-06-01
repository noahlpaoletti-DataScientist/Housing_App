import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import PropertyReport from "./pages/PropertyReport";
import RenovationCalculator from "./pages/RenovationCalculator";
import InvestorCalculator from "./pages/InvestorCalculator";
import AdminDashboard from "./pages/AdminDashboard";

const navItems = [
  { to: "/", label: "Search" },
  { to: "/report", label: "Report" },
  { to: "/renovation", label: "Renovation" },
  { to: "/investor", label: "Investor" },
  { to: "/admin", label: "Admin" },
];

export default function App() {
  return (
    <div className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />
      <header className="site-header">
        <Link to="/" className="brand-mark">
          PropLens Intelligence
        </Link>
        <nav className="nav-row">
          {navItems.map((item) => (
            <Link key={item.to} to={item.to} className="nav-link">
              {item.label}
            </Link>
          ))}
        </nav>
      </header>

      <main className="page-shell">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/report" element={<PropertyReport />} />
          <Route path="/renovation" element={<RenovationCalculator />} />
          <Route path="/investor" element={<InvestorCalculator />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </main>
    </div>
  );
}
