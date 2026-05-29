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

  const [selectedDate, setSelectedDate] = useState("2026-05-29");
  const [content, setContent] = useState("");
  const [nickname, setNickname] = useState("");
  const [diaryDates, setDiaryDates] = useState([]);
  const [diaryId, setDiaryId] = useState(null);

  const formatDateText = (dateString) => {
    const date = new Date(dateString);
    const weekDays = [
      "일요일",
      "월요일",
      "화요일",
      "수요일",
      "목요일",
      "금요일",
      "토요일",
    ];

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}.${month}.${day} ${weekDays[date.getDay()]}`;
  };

  const getDiaryDates = async () => {
    try {
      const response = await api.get("/api/diaries/dates");
      setDiaryDates(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const getDiaryByDate = async (date) => {
    try {
      const response = await api.get(`/api/diaries/date/${date}`);

      setContent(response.data.content);
      setDiaryId(response.data.id);
      setIsEditMode(false);
    } catch (error) {
      setContent("");
      setDiaryId(null);
      setIsEditMode(true);
    }
  };

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

  useEffect(() => {
    getDiaryDates();
  }, []);

  useEffect(() => {
    getDiaryByDate(selectedDate);
  }, [selectedDate]);

  const handleSave = async () => {
    if (!content.trim()) {
      alert("일기 내용을 입력해 주세요.");
      return;
    }

    try {
      const requestData = {
        content,
        diary_date: selectedDate,
      };

      if (diaryId) {
        await api.patch(`/api/diaries/date/${selectedDate}`, requestData);
      } else {
        await api.post("/api/diaries", requestData);
      }

      await getDiaryByDate(selectedDate);
      await getDiaryDates();

      alert("일기 저장 성공");
    } catch (error) {
      console.error(error);
      console.error(error.response?.data);
      alert("일기 저장 실패");
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

          <span className="date-text">{formatDateText(selectedDate)}</span>
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
                <span className="profile-name">{nickname || "사용자"}</span>
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
          diaryDates={diaryDates}
          onClose={() => setIsCalendarOpen(false)}
        />
      )}
    </MobileLayout>
  );
}

export default MainPage;