import { useNavigate } from "react-router-dom";
import "../styles/UserPage.css";

function SignUpPage() {
  const navigate = useNavigate();

  return (
    <div className="user-layout">
      <div className="user-screen">
        <div className="user-page">
          <h1 className="user-title">SIGN UP PAGE</h1>

          <div className="signup-form">
            <label className="user-label">이메일</label>
            <input className="user-input" type="email" placeholder="Email" />

            <label className="user-label">닉네임</label>
            <input className="user-input" type="text" placeholder="NickName" />

            <label className="user-label">비밀번호</label>
            <input
              className="user-input"
              type="password"
              placeholder="PassWord"
            />

            <label className="user-label">비밀번호 확인</label>
            <input
              className="user-input"
              type="password"
              placeholder="PassWord Confirm"
            />

            <button
              className="signup-submit-button"
              onClick={() => navigate("/login")}
            >
              SIGN UP
            </button>

            <p className="login-guide">Already have an account?</p>

            <button
              className="login-move-button"
              onClick={() => navigate("/login")}
            >
              LOGIN
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignUpPage;