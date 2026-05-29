// import { useNavigate } from "react-router-dom";
// import "../styles/UserPage.css";

// function SignUpPage() {
//   const navigate = useNavigate();

//   return (
//     <div className="user-layout">
//       <div className="user-screen">
//         <div className="user-page">
//           <h1 className="user-title">SIGN UP PAGE</h1>

//           <div className="signup-form">
//             <label className="user-label">이메일</label>
//             <input className="user-input" type="email" placeholder="Email" />

//             <label className="user-label">닉네임</label>
//             <input className="user-input" type="text" placeholder="NickName" />

//             <label className="user-label">비밀번호</label>
//             <input
//               className="user-input"
//               type="password"
//               placeholder="PassWord"
//             />

//             <label className="user-label">비밀번호 확인</label>
//             <input
//               className="user-input"
//               type="password"
//               placeholder="PassWord Confirm"
//             />

//             <button
//               className="signup-submit-button"
//               onClick={() => navigate("/login")}
//             >
//               SIGN UP
//             </button>

//             <p className="login-guide">Already have an account?</p>

//             <button
//               className="login-move-button"
//               onClick={() => navigate("/login")}
//             >
//               LOGIN
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default SignUpPage;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../shared/api/axios";
import "../styles/UserPage.css";

function SignUpPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [nickname, setNickname] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  const handleSignUp = async () => {
    if (password !== passwordConfirm) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      await api.post("/api/users/signup", {
        email,
        nickname,
        password,
      });

      alert("회원가입 성공");
      navigate("/login");
    } catch (error) {
      console.error(error);
      alert("회원가입 실패");
    }
  };

  return (
    <div className="user-layout">
      <div className="user-screen">
        <div className="user-page">
          <h1 className="user-title">SIGN UP PAGE</h1>

          <div className="signup-form">
            <label className="user-label">이메일</label>
            <input
              className="user-input"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <label className="user-label">닉네임</label>
            <input
              className="user-input"
              type="text"
              placeholder="NickName"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
            />

            <label className="user-label">비밀번호</label>
            <input
              className="user-input"
              type="password"
              placeholder="PassWord"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <label className="user-label">비밀번호 확인</label>
            <input
              className="user-input"
              type="password"
              placeholder="PassWord Confirm"
              value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)}
            />

            <button className="signup-submit-button" onClick={handleSignUp}>
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