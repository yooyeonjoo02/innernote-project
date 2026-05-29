import React from 'react';

function StatisticsSummary({ statData, viewType }) {
  return (
    <div className="bg-white/60 text-center p-4 rounded-2xl border border-orange-100/20 text-xs text-gray-500 leading-relaxed">
      총 {statData.total_diary_count}개의 일기를 기준으로 계산한{' '}
      {viewType === 'weekly' ? '주별' : '월별'} 평균 감정 통계입니다.
    </div>
  );
}

export default StatisticsSummary;