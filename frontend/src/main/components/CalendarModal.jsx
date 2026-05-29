import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

function CalendarModal({ selectedDate, setSelectedDate, diaryDates, onClose }) {
  const selected = new Date(selectedDate);

  const [currentYear, setCurrentYear] = useState(selected.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(selected.getMonth() + 1);

  const getDateString = (year, month, day) => {
    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
  };

  const lastDay = new Date(currentYear, currentMonth, 0).getDate();
  const firstDayOfWeek = new Date(currentYear, currentMonth - 1, 1).getDay();

  const days = Array.from({ length: lastDay }, (_, i) => i + 1);
  const emptyDays = Array.from({ length: firstDayOfWeek });

  const selectedDay = selected.getDate();
  const selectedYear = selected.getFullYear();
  const selectedMonth = selected.getMonth() + 1;

  const handleSelectDate = (day) => {
    const date = getDateString(currentYear, currentMonth, day);
    setSelectedDate(date);
    onClose();
  };

  const handlePrevMonth = () => {
    if (currentMonth === 1) {
      setCurrentYear((prev) => prev - 1);
      setCurrentMonth(12);
    } else {
      setCurrentMonth((prev) => prev - 1);
    }
  };

  const handleNextMonth = () => {
    if (currentMonth === 12) {
      setCurrentYear((prev) => prev + 1);
      setCurrentMonth(1);
    } else {
      setCurrentMonth((prev) => prev + 1);
    }
  };

  return (
    <div className="calendar-overlay">
      <div className="calendar-box">
        <div className="calendar-top">
          <button className="calendar-arrow-button" onClick={handlePrevMonth}>
            <ChevronLeft size={20} />
          </button>

          <select
            value={currentMonth}
            className="calendar-select"
            onChange={(e) => setCurrentMonth(Number(e.target.value))}
          >
            {Array.from({ length: 12 }, (_, i) => i + 1).map((month) => (
              <option key={month} value={month}>
                {month}월
              </option>
            ))}
          </select>

          <input
            className="calendar-year-input"
            type="number"
            value={currentYear}
            onChange={(e) => setCurrentYear(Number(e.target.value))}
          />

          <button className="calendar-arrow-button" onClick={handleNextMonth}>
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
          {emptyDays.map((_, index) => (
            <div key={`empty-${index}`} />
          ))}

          {days.map((day) => {
            const date = getDateString(currentYear, currentMonth, day);
            const hasDiary = diaryDates.includes(date);

            const isSelected =
              currentYear === selectedYear &&
              currentMonth === selectedMonth &&
              day === selectedDay;

            let buttonClassName = "date-button no-diary";

            if (hasDiary) {
              buttonClassName = "date-button has-diary";
            }

            if (isSelected) {
              buttonClassName = "date-button active";
            }

            return (
              <button
                key={day}
                className={buttonClassName}
                onClick={() => handleSelectDate(day)}
              >
                {day}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default CalendarModal;