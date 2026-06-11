import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../shared/api/axios";
import "../styles/UserPage.css";

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await api.post("/api/users/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", response.data.access_token);

      alert("로그인 성공");
      navigate("/main");
    } catch (error) {
      console.error(error);
      alert("로그인 실패");
    }
  };

  return (
    <div className="user-layout">
      <div className="user-screen">
        <div className="user-page">
          <h1 className="user-title login-title">LOGIN PAGE</h1>

          <div className="login-form">
            <input
              className="user-input"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              className="user-input"
              type="password"
              placeholder="PassWord"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              className="forgot-button"
              onClick={() => navigate("/forgot-password")}
            >
              Forgot Password?
            </button>

            <div className="login-button-row">
              <button
                className="user-button pink"
                onClick={() => navigate("/signup")}
              >
                SIGN UP
              </button>

              <button className="user-button light-pink" onClick={handleLogin}>
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