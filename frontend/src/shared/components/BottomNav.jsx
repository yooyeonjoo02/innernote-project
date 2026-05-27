import { NavLink } from "react-router-dom";
import {
  Compass,
  Home,
  User
} from "lucide-react";

import "./BottomNav.css";

function BottomNav() {
  return (
    <nav className="bottom-nav">

      {/* 왼쪽 */}
      <NavLink to="/statistics" className="nav-item">
        <Compass size={24} strokeWidth={2.2} />
      </NavLink>

      {/* 가운데 */}
      <NavLink to="/" end className="nav-item">
        <Home
          size={25}
          fill="currentColor"
          stroke="none"
        />
      </NavLink>

      {/* 오른쪽 */}
      <NavLink to="/survey" className="nav-item">
        <User size={25} strokeWidth={2.2} />
      </NavLink>

    </nav>
  );
}

export default BottomNav;