import React, { useState, useEffect } from 'react';
import './StatisticsPage.css';

import {
  ChevronLeft,
  ChevronRight,
  Play,
  MapPin,
  Music,
  CheckCircle,
  BarChart2
} from 'lucide-react';

import MobileLayout from '../../shared/components/MobileLayout';

function StatisticsPage() {
  const [selectedDate, setSelectedDate] = useState('2026-05-21'); 
  const [viewType, setViewType] = useState('daily');             
  const [periodDays, setPeriodDays] = useState(7);               

  const [statData, setStatData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStatistics = async () => {
    setLoading(true);
    setError(null);
    try {
      let url = '';
      if (viewType === 'daily') {
        url = `http://127.0.0.1:8000/api/v1/statistics/daily?date=${selectedDate}`;
      } else {
        url = `http://127.0.0.1:8000/api/v1/statistics/period?date=${selectedDate}&period=${periodDays}`;
      }

      const response = await fetch(url);
      if (!response.ok) throw new Error('백엔드 서버 통신 실패');
      
      const result = await response.json();
      if (result.status === 'success') {
        setStatData(result.data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatistics();
  }, [selectedDate, viewType, periodDays]);

  const emotionColorMap = {
    '행복': '#ffedd5',
    '평범': '#fef08a',
    '놀람': '#ccfbf1',
    '슬픔': '#fbcfe8',
    '분노': '#fca5a5',
    '혐오': '#99f6e4'
  };

  const getEmotionBgClass = (name) => {
    const classes = {
      '행복': 'bg-[#ffedd5]',
      '평범': 'bg-[#fef08a]',
      '놀람': 'bg-[#ccfbf1]',
      '슬픔': 'bg-[#fbcfe8]',
      '분노': 'bg-[#fca5a5]',
      '혐오': 'bg-[#99f6e4]'
    };
    return classes[name] || 'bg-gray-200';
  };

  const getEmotionEmoji = (name) => {
    const emojis = { '행복': '😊', '평범': '😐', '놀람': '😲', '슬픔': '😢', '분노': '😡', '혐오': '🤢' };
    return emojis[name] || '🤍';
  };

  const emotionsList = statData?.emotion_analysis || statData?.aggregated_emotion_analysis || [];
  
  const activeEmotions = emotionsList.filter(e => e.ratio > 0);
  let accumulatedPercent = 0;
  
  const chartSegments = activeEmotions.map(emo => {
    const start = accumulatedPercent;
    accumulatedPercent += emo.ratio;
    const color = emotionColorMap[emo.emotion_name] || '#e5e7eb';
    return `${color} ${start}% ${accumulatedPercent}%`;
  });

  const donutChartStyle = chartSegments.length > 0
    ? { background: `conic-gradient(${chartSegments.join(', ')})` }
    : { background: '#e5e7eb' };

  const dominantEmotion = emotionsList.reduce((max, current) => 
    current.ratio > max.ratio ? current : max, 
    { emotion_name: '대기', ratio: 0 }
  );

  const displayDate = statData?.diary_info?.diary_date || selectedDate;
  const recs = statData?.recommendations;
  return (
    <MobileLayout>
      <div className="flex flex-col h-full bg-[#fff5f0]">
        
        <header className="pt-6 pb-2 px-6">
          <h1 className="text-xl font-bold text-center text-gray-900 tracking-tight">
            InnerNote
          </h1>

          <div className="flex gap-2 mt-4 border-b border-orange-100/50">
            <button 
              onClick={() => setViewType('daily')}
              className={`pb-2 px-3 text-sm transition-all ${viewType === 'daily' ? 'font-bold border-b-2 border-red-400 text-red-500' : 'font-medium text-gray-400 hover:text-gray-600'}`}
            >
              일별
            </button>

            <button 
              onClick={() => { setViewType('period'); setPeriodDays(7); }}
              className={`pb-2 px-3 text-sm transition-all ${viewType === 'period' && periodDays === 7 ? 'font-bold border-b-2 border-red-400 text-red-500' : 'font-medium text-gray-400 hover:text-gray-600'}`}
            >
              주별
            </button>

            <button 
              onClick={() => { setViewType('period'); setPeriodDays(30); }}
              className={`pb-2 px-3 text-sm transition-all ${viewType === 'period' && periodDays === 30 ? 'font-bold border-b-2 border-red-400 text-red-500' : 'font-medium text-gray-400 hover:text-gray-600'}`}
            >
              월별
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto pb-24 px-5 pt-4">

          {loading && <div className="text-center text-xs text-gray-500 mb-4 animate-pulse">감정 분석 스트림 로딩 중...</div>}
          {error && <div className="text-center text-xs text-red-500 mb-4">백엔드 서버 오프라인: {error}</div>}

          {!loading && statData && (
            <>
              <div className="flex justify-between items-center mb-5 px-2">
                <button className="p-1 rounded-full hover:bg-orange-100 transition">
                  <ChevronLeft className="w-5 h-5 text-gray-600" />
                </button>

                <span className="text-sm font-semibold text-gray-700">
                  {viewType === 'daily' ? displayDate : `최근 ${periodDays}일 대시보드 (기준: ${selectedDate})`}
                </span>

                <button className="p-1 rounded-full hover:bg-orange-100 transition">
                  <ChevronRight className="w-5 h-5 text-gray-600" />
                </button>
              </div>

              <div className="bg-white p-5 rounded-3xl shadow-sm border border-orange-100/30 mb-5">
                <div className="flex justify-between items-center mb-4">
                  <div className="flex items-center gap-1.5">
                    <BarChart2 className="w-4 h-4 text-purple-500" />
                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                      {viewType === 'daily' ? 'Hugging Face 감정 분석' : '기간 누적 감정 통계'}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between gap-4">
                  <div 
                    style={donutChartStyle}
                    className="relative w-36 h-36 rounded-full flex items-center justify-center emotion-chart shrink-0 shadow-sm transition-all duration-500"
                  >
                    <div className="absolute w-24 h-24 bg-white rounded-full flex flex-col items-center justify-center shadow-inner">
                      <span className="text-xl mb-0.5">{getEmotionEmoji(dominantEmotion.emotion_name)}</span>
                      <span className="font-extrabold text-gray-800 text-sm">{dominantEmotion.emotion_name}</span>
                      <span className="text-gray-500 font-bold text-xs">{dominantEmotion.ratio}%</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-x-3 gap-y-2 flex-1 text-xs">
                    {emotionsList.map((emo, idx) => (
                      <div key={idx} className="flex items-center gap-1.5 text-gray-600 font-medium">
                        <span className={`w-2.5 h-2.5 rounded-full ${getEmotionBgClass(emo.emotion_name)} border border-gray-200/50`}></span>
                        <span className={emo.ratio > 0 ? "font-bold text-gray-800" : ""}>
                          {emo.emotion_name} {emo.ratio > 0 && `${emo.ratio}%`}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {viewType === 'daily' && recs && (
                <>
                  <h2 className="text-base font-bold text-gray-800 mb-3 px-1 flex items-center gap-1">
                    ✨ 오늘의 맞춤형 추천
                  </h2>

                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white shadow-sm border border-blue-100/30 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]">
                        <div className="flex items-center gap-1 text-blue-700 font-bold text-xs mb-2">
                          <MapPin className="w-3.5 h-3.5" />
                          <span>추천 장소</span>
                        </div>
                        <div>
                          <p className="font-extrabold text-gray-800 text-sm leading-snug">{recs.place.place_name}</p>
                          <p className="text-[11px] text-gray-500 mt-1 font-medium">{recs.place.address}</p>
                        </div>
                      </div>

                      <div className="bg-white shadow-sm border border-purple-100/30 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]">
                        <div className="flex items-center gap-1 text-purple-700 font-bold text-xs mb-2">
                          <Music className="w-3.5 h-3.5" />
                          <span>오늘의 음악</span>
                        </div>
                        <div className="space-y-2">
                          {recs.playlist.map((music) => (
                            <a 
                              href={music.youtube_url} 
                              target="_blank" 
                              rel="noreferrer" 
                              key={music.music_id} 
                              className="flex items-center gap-1.5 text-xs text-gray-700 group cursor-pointer block"
                            >
                              <Play className="w-3 h-3 text-gray-500 fill-gray-500 group-hover:text-purple-600 group-hover:fill-purple-600 shrink-0" />
                              <span className="truncate font-medium group-hover:text-purple-600">{music.title}</span>
                            </a>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="bg-white shadow-sm border border-emerald-100/30 rounded-2xl p-4">
                      <div className="flex items-center gap-1 text-emerald-700 font-bold text-xs mb-1.5">
                        <CheckCircle className="w-3.5 h-3.5" />
                        <span>오늘의 미션 ({recs.mission.mission_type})</span>
                      </div>
                      <p className="text-xs text-gray-700 font-semibold leading-relaxed">"{recs.mission.mission_content}"</p>
                    </div>
                  </div>
                </>
              )}

              {viewType === 'period' && (
                <div className="bg-white/60 text-center p-4 rounded-2xl border border-orange-100/20 text-xs text-gray-500 leading-relaxed">
                  {statData.description}
                </div>
              )}
            </>
          )}
        </main>
      </div>
    </MobileLayout>
  );
}

export default StatisticsPage;