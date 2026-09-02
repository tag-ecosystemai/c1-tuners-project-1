import { Link, useLocation } from "react-router-dom";
import { Leaf, LayoutDashboard, ScanLine, History } from "lucide-react";

function Navbar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="logo">
        <div className="logo-icon">
          <Leaf size={24} />
        </div>

        <div>
          <h2>Potato</h2>
          <span>Leaf Classification</span>
        </div>
      </div>

      <nav className="nav-menu">
        <Link
          to="/"
          className={location.pathname === "/" ? "nav-link active" : "nav-link"}
        >
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </Link>

        <Link
          to="/analyze"
          className={
            location.pathname === "/analyze"
              ? "nav-link active"
              : "nav-link"
          }
        >
          <ScanLine size={20} />
          <span>Analyze Leaf</span>
        </Link>

        <Link
          to="/history"
          className={
            location.pathname === "/history"
              ? "nav-link active"
              : "nav-link"
          }
        >
          <History size={20} />
          <span>History</span>
        </Link>
      </nav>

    </aside>
  );
}

export default Navbar;