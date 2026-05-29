import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

import MobileLayout from '../../shared/components/MobileLayout';

import StatisticsHeader from '../components/StatisticsHeader';
import EmotionChart from '../components/EmotionChart';
import RecommendationCard from '../components/RecommendationCard';
import StatisticsSummary from '../components/StatisticsSummary';

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

  const { statData, loading, error } = useStatistics(selectedDate, viewType);

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
              />

              {viewType === 'daily' && statData.recommendations && (
                <RecommendationCard recs={statData.recommendations} />
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
      </div>
    </MobileLayout>
  );
}

export default StatisticsPage;