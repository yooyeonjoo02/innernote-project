import BottomNav from "./BottomNav";
import "../styles/mobile-layout.css";

function MobileLayout({ children, backgroundClass = "" }) {
  return (
    <div className="app-container">
      <div className={`mobile-frame ${backgroundClass}`}>

        <div className="mobile-content">
          {children}
        </div>

        <BottomNav />
      </div>
    </div>
  );
}

export default MobileLayout;

