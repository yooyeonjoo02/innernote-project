import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../shared/api/axios";
import "../styles/UserPage.css";

function ResetPasswordPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const email = location.state?.email || "";

  const [newPassword, setNewPassword] = useState("");
  const [passwordCheck, setPasswordCheck] = useState("");

  const handleResetPassword = async () => {
    if (!email) {
      alert("이메일 정보가 없습니다. 다시 시도해 주세요.");
      navigate("/forgot-password");
      return;
    }

    if (!newPassword.trim()) {
      alert("새 비밀번호를 입력해 주세요.");
      return;
    }

    if (newPassword !== passwordCheck) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      await api.post("/api/users/reset-password", {
        email,
        new_password: newPassword,
      });

      alert("비밀번호가 변경되었습니다. 다시 로그인해 주세요.");
      navigate("/login");
    } catch (error) {
      console.error(error);
      alert("비밀번호 변경 실패");
    }
  };

  return (
    <div className="user-layout">
      <div className="user-screen">
        <div className="user-page">
          <h1 className="user-title login-title">RESET PASSWORD</h1>

          <div className="login-form">
            <input
              className="user-input"
              type="email"
              value={email}
              disabled
            />

            <input
              className="user-input"
              type="password"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />

            <input
              className="user-input"
              type="password"
              placeholder="Check Password"
              value={passwordCheck}
              onChange={(e) => setPasswordCheck(e.target.value)}
            />

            <div className="login-button-row">
              <button
                className="user-button pink"
                onClick={() => navigate("/forgot-password")}
              >
                BACK
              </button>

              <button
                className="user-button light-pink"
                onClick={handleResetPassword}
              >
                RESET
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResetPasswordPage;