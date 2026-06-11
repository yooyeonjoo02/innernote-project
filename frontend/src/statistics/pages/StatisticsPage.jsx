import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

import MobileLayout from '../../shared/components/MobileLayout';

import StatisticsHeader from '../components/StatisticsHeader';
import EmotionChart from '../components/EmotionChart';
import RecommendationCard from '../components/RecommendationCard';
import StatisticsSummary from '../components/StatisticsSummary';
import CalendarModal from '../../main/components/CalendarModal';

import useStatistics from '../hooks/useStatistics';
import { getChangedDate } from '../utils/dateUtils';

function StatisticsPage() {
  const location = useLocation();

  const getTodayString = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const [selectedDate, setSelectedDate] = useState(
    location.state?.selectedDate || getTodayString()
  );

  const [viewType, setViewType] = useState('daily');
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [diaryDates, setDiaryDates] = useState([]);

  const {
    statData,
    recommendation,
    loading,
    recommendationLoading,
    error,
    recommendationError
  } = useStatistics(selectedDate, viewType);

  useEffect(() => {
    const fetchDiaryDates = async () => {
      try {
        const token =
          localStorage.getItem('accessToken') ||
          localStorage.getItem('token') ||
          localStorage.getItem('access_token');

        if (!token) {
          setDiaryDates([]);
          return;
        }

        const response = await fetch('http://localhost:8000/api/diaries', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (!response.ok) {
          setDiaryDates([]);
          return;
        }

        const data = await response.json();

        const dates = data
          .map((diary) => {
            if (diary.diary_date) return diary.diary_date;
            if (diary.created_at) return diary.created_at.slice(0, 10);
            if (diary.date) return diary.date;
            return null;
          })
          .filter(Boolean);

        setDiaryDates(dates);
      } catch (error) {
        console.error('diaryDates fetch error:', error);
        setDiaryDates([]);
      }
    };

    fetchDiaryDates();
  }, []);

  const changeDate = (amount) => {
    const newDate = getChangedDate(selectedDate, viewType, amount);
    setSelectedDate(newDate);
  };

  return (
    <MobileLayout>
      <div className="flex flex-col h-full bg-[#fff5f0]">
        <StatisticsHeader
          viewType={viewType}
          setViewType={setViewType}
        />

        <main className="flex-1 overflow-y-auto pb-24 px-5 pt-4">
          {loading && (
            <div className="text-center text-xs text-gray-500 mb-4 animate-pulse">
              감정 분석 스트림 로딩 중...
            </div>
          )}

          {error && (
            <div className="text-center text-xs text-red-500 mb-4">
              백엔드 서버 오프라인: {error}
            </div>
          )}

          {!loading && statData && (
            <>
              <EmotionChart
                statData={statData}
                viewType={viewType}
                selectedDate={selectedDate}
                changeDate={changeDate}
                onOpenCalendar={() => setIsCalendarOpen(true)}
              />

              {viewType === 'daily' && recommendationLoading && (
                <div className="text-center text-xs text-gray-500 my-4 animate-pulse">
                  추천 결과 불러오는 중...
                </div>
              )}

              {viewType === 'daily' && recommendationError && (
                <div className="text-center text-xs text-red-500 my-4">
                  추천 결과를 불러오지 못했습니다: {recommendationError}
                </div>
              )}

              {viewType === 'daily' && recommendation && (
                <RecommendationCard recommendation={recommendation} />
              )}

              {(viewType === 'weekly' || viewType === 'monthly') && (
                <StatisticsSummary
                  statData={statData}
                  viewType={viewType}
                />
              )}
            </>
          )}
        </main>

        {isCalendarOpen && (
          <CalendarModal
            selectedDate={selectedDate}
            setSelectedDate={setSelectedDate}
            diaryDates={diaryDates}
            onClose={() => setIsCalendarOpen(false)}
          />
        )}
      </div>
    </MobileLayout>
  );
}

export default StatisticsPage;