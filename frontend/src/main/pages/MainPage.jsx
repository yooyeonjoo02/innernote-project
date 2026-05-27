import { useEffect, useState } from "react";
import { Calendar, Edit3, Menu } from "lucide-react";
import { useNavigate } from "react-router-dom";
import MobileLayout from "../../shared/components/MobileLayout";
import CalendarModal from "../components/CalendarModal";
import api from "../../shared/api/axios";
import "./MainPage.css";

function MainPage() {
  const navigate = useNavigate();

  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(true);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const [selectedDate, setSelectedDate] = useState("2026.05.05 화요일");
  const [content, setContent] = useState("");
  const [nickname, setNickname] = useState("");

  useEffect(() => {
    const getMyInfo = async () => {
      try {
        const response = await api.get("/api/users/me");
        setNickname(response.data.nickname);
      } catch (error) {
        console.error(error);
        alert("로그인이 필요합니다.");
        navigate("/login");
      }
    };

    getMyInfo();
  }, [navigate]);

  const handleSave = async () => {
    if (!content.trim()) {
      alert("일기 내용을 입력해 주세요.");
      return;
    }

    try {
      await api.post("/api/diaries", {
        content,
        emotion: "neutral",
      });

      alert("일기 저장 성공");
      setIsEditMode(false);
    } catch (error) {
      console.error(error);
      alert("일기 저장 실패. 다시 로그인해 주세요.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsMenuOpen(false);
    navigate("/login");
  };

  return (
    <MobileLayout backgroundClass="main-bg">
      <header className="main-header">
        <div className="date-area">
          <button
            className="icon-button"
            onClick={() => setIsCalendarOpen(true)}
          >
            <Calendar size={22} />
          </button>

          <span className="date-text">{selectedDate}</span>
        </div>

        <div className="header-actions">
          <button
            className="square-button"
            onClick={() => {
              setIsEditMode(true);
              setIsMenuOpen(false);
            }}
          >
            <Edit3 size={20} />
          </button>

          <button
            className="square-button"
            onClick={() => setIsMenuOpen((prev) => !prev)}
          >
            <Menu size={25} />
          </button>

          {isMenuOpen && (
            <div className="menu-dropdown">
              <div className="profile-row">
                <div className="profile-icon">🙂</div>
                <span className="profile-name">
                  {nickname || "사용자"}
                </span>
              </div>

              <button className="logout-button" onClick={handleLogout}>
                LOGOUT
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="diary-area">
        {isEditMode ? (
          <textarea
            className="diary-edit-box"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="오늘 하루는 어땠나요?"
          />
        ) : (
          <div className="diary-text">{content}</div>
        )}
      </main>

      {isEditMode && (
        <button className="save-button" onClick={handleSave}>
          Save
        </button>
      )}

      {isCalendarOpen && (
        <CalendarModal
          selectedDate={selectedDate}
          setSelectedDate={setSelectedDate}
          onClose={() => setIsCalendarOpen(false)}
        />
      )}
    </MobileLayout>
  );
}

export default MainPage;