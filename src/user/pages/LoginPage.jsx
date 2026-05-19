import { useNavigate } from "react-router-dom";
import "../styles/UserPage.css";

function LoginPage() {
  const navigate = useNavigate();

  return (
    <div className="user-layout">
      <div className="user-screen">
        <div className="user-page">
          <h1 className="user-title login-title">LOGIN PAGE</h1>

          <div className="login-form">
            <input className="user-input" type="email" placeholder="Email" />
            <input
              className="user-input"
              type="password"
              placeholder="PassWord"
            />

            <button className="forgot-button">Forgot Password?</button>

            <div className="login-button-row">
              <button
                className="user-button pink"
                onClick={() => navigate("/signup")}
              >
                SIGN UP
              </button>

              <button
                className="user-button light-pink"
                onClick={() => navigate("/main")}
              >
                LOGIN
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;