import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../shared/api/axios";
import "../styles/UserPage.css";

function ForgotPasswordPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const handleForgotPassword = async () => {
    if (!email.trim()) {
      alert("이메일을 입력해 주세요.");
      return;
    }

    try {
      await api.post("/api/users/forgot-password", {
        email,
      });

      alert("이메일 확인 완료. 새 비밀번호를 설정해 주세요.");

      navigate("/reset-password", {
        state: {
          email,
        },
      });
    } catch (error) {
      console.error(error);
      alert("가입된 이메일을 찾을 수 없습니다.");
    }
  };

  return (
    <div className="user-layout">
      <div className="user-screen">
        <div className="user-page">
          <h1 className="user-title login-title">FORGOT PASSWORD</h1>

          <div className="login-form">
            <input
              className="user-input"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <div className="login-button-row">
              <button
                className="user-button pink"
                onClick={() => navigate("/login")}
              >
                BACK
              </button>

              <button
                className="user-button light-pink"
                onClick={handleForgotPassword}
              >
                NEXT
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ForgotPasswordPage;