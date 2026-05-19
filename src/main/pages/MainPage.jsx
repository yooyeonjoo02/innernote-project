import { useState } from "react";
import { Calendar, Edit3, Menu } from "lucide-react";
import { useNavigate } from "react-router-dom";
import MobileLayout from "../../shared/components/MobileLayout";
import CalendarModal from "../components/CalendarModal";
import "./MainPage.css";

const initialDiary = `오늘은 하루 종일 이상하게 마음이 편안했다.
특별한 일이 있었던 건 아닌데, 날씨도 좋고
바람도 적당해서 그냥 걷는 것만으로도 기분이 꽤 좋았다.
오랜만에 혼자 카페에 가서 창가 자리에 앉았는데, 사람들이 바쁘게 지나가는 걸 멍하니 보고 있으니까 시간 가는 줄 몰랐다.
이런 아무 생각 없이 보내는 시간이 요즘 나한테는 꽤 소중한 것 같다.`;

function MainPage() {
  const navigate = useNavigate();

  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const [selectedDate, setSelectedDate] = useState("2026.05.05 화요일");
  const [content, setContent] = useState(initialDiary);

  const handleSave = () => {
    setIsEditMode(false);
  };

  const handleLogout = () => {
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
                <span className="profile-name">행복이</span>
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