import { Routes, Route, Navigate } from "react-router-dom";

import MainPage from "./main/pages/MainPage";
import StatisticsPage from "./statistics/pages/StatisticsPage";
import SurveyPage from "./survey/pages/SurveyPage";

import LoginPage from "./user/pages/LoginPage";
import SignUpPage from "./user/pages/SignUpPage";
import ForgotPasswordPage from "./user/pages/ForgotPasswordPage";
import ResetPasswordPage from "./user/pages/ResetPasswordPage";


function App() {
  return (
    <Routes>
      {/* 시작하면 로그인 페이지로 */}
      <Route path="/" element={<Navigate to="/main" />} />

      {/* User */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      {/* Main */}
      <Route path="/main" element={<MainPage />} />
      <Route path="/statistics" element={<StatisticsPage />} />
      <Route path="/survey" element={<SurveyPage />} />
    </Routes>
  );
}

export default App;
