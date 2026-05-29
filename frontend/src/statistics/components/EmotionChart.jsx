import React from 'react';

import {
  ChevronLeft,
  ChevronRight,
  BarChart2
} from 'lucide-react';

import EmotionLegend from './EmotionLegend';

import {
  emotionColorMap,
  getEmotionEmoji
} from '../utils/emotionUtils';

function EmotionChart({
  statData,
  viewType,
  selectedDate,
  changeDate
}) {
  const getCurrentEmotionList = () => {
    if (!statData) return [];

    if (viewType === 'daily') {
      return statData.emotion_analysis || [];
    }

    return statData.average_emotions || [];
  };

  const emotionsList = getCurrentEmotionList();

  const activeEmotions = emotionsList.filter(
    (emotion) => emotion.ratio > 0
  );

  let accumulatedPercent = 0;

  const chartSegments = activeEmotions.map((emotion) => {
    const start = accumulatedPercent;
    accumulatedPercent += emotion.ratio;

    const color =
      emotionColorMap[emotion.emotion_name] || '#e5e7eb';

    return `${color} ${start}% ${accumulatedPercent}%`;
  });

  const donutChartStyle =
    chartSegments.length > 0
      ? {
          background: `conic-gradient(${chartSegments.join(', ')})`
        }
      : {
          background: '#e5e7eb'
        };

  const dominantEmotion = statData?.dominant_emotion
    ? {
        emotion_name: statData.dominant_emotion,
        ratio:
          emotionsList.find(
            (emotion) =>
              emotion.emotion_name === statData.dominant_emotion
          )?.ratio || 0
      }
    : emotionsList.reduce(
        (max, current) =>
          current.ratio > max.ratio ? current : max,
        { emotion_name: '대기', ratio: 0 }
      );

  const getTitleText = () => {
    if (viewType === 'daily') {
      return statData?.diary_info?.diary_date || selectedDate;
    }

    if (viewType === 'weekly') {
      return `${statData?.start_date || ''} ~ ${statData?.end_date || ''}`;
    }

    if (viewType === 'monthly') {
      return `${statData?.start_date || ''} ~ ${statData?.end_date || ''}`;
    }

    return selectedDate;
  };

  const getChartTitle = () => {
    if (viewType === 'daily') {
      return 'Hugging Face 감정 분석';
    }

    if (viewType === 'weekly') {
      return '주별 평균 감정 통계';
    }

    if (viewType === 'monthly') {
      return '월별 평균 감정 통계';
    }

    return '감정 통계';
  };

  return (
    <>
      <div className="flex justify-between items-center mb-5 px-2">
        <button
          onClick={() => changeDate(-1)}
          className="p-1 rounded-full hover:bg-orange-100 transition"
        >
          <ChevronLeft className="w-5 h-5 text-gray-600" />
        </button>

        <span className="text-sm font-semibold text-gray-700 text-center">
          {getTitleText()}
        </span>

        <button
          onClick={() => changeDate(1)}
          className="p-1 rounded-full hover:bg-orange-100 transition"
        >
          <ChevronRight className="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div className="bg-white p-5 rounded-3xl shadow-sm border border-orange-100/30 mb-5">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-1.5">
            <BarChart2 className="w-4 h-4 text-purple-500" />
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
              {getChartTitle()}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between gap-4">
          <div
            style={donutChartStyle}
            className="relative w-36 h-36 rounded-full flex items-center justify-center emotion-chart shrink-0 shadow-sm transition-all duration-500"
          >
            <div className="absolute w-24 h-24 bg-white rounded-full flex flex-col items-center justify-center shadow-inner">
              <span className="text-xl mb-0.5">
                {getEmotionEmoji(dominantEmotion.emotion_name)}
              </span>

              <span className="font-extrabold text-gray-800 text-sm">
                {dominantEmotion.emotion_name}
              </span>

              <span className="text-gray-500 font-bold text-xs">
                {dominantEmotion.ratio}%
              </span>
            </div>
          </div>

          <EmotionLegend emotionsList={emotionsList} />
        </div>
      </div>
    </>
  );
}

export default EmotionChart;