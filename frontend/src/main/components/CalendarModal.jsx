import { ChevronLeft, ChevronRight } from "lucide-react";

const days = Array.from({ length: 30 }, (_, i) => i + 1);

function CalendarModal({ selectedDate, setSelectedDate, onClose }) {
  const handleSelectDate = (day) => {
    setSelectedDate(`2026.05.${String(day).padStart(2, "0")} 화요일`);
    onClose();
  };

  const selectedDay = Number(selectedDate?.split(".")[2]?.split(" ")[0]);

  return (
    <div className="calendar-overlay">
      <div className="calendar-box">
        <div className="calendar-top">
          <button className="calendar-arrow-button">
            <ChevronLeft size={20} />
          </button>

          <select defaultValue="May" className="calendar-select">
            <option>May</option>
            <option>Jun</option>
            <option>Sep</option>
          </select>

          <select defaultValue="2026" className="calendar-select">
            <option>2025</option>
            <option>2026</option>
          </select>

          <button className="calendar-arrow-button">
            <ChevronRight size={20} />
          </button>
        </div>

        <div className="week-row">
          <span>Su</span>
          <span>Mo</span>
          <span>Tu</span>
          <span>We</span>
          <span>Th</span>
          <span>Fr</span>
          <span>Sa</span>
        </div>

        <div className="date-grid">
          {days.map((day) => (
            <button
              key={day}
              className={
                day === selectedDay ? "date-button active" : "date-button"
              }
              onClick={() => handleSelectDate(day)}
            >
              {day}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CalendarModal;