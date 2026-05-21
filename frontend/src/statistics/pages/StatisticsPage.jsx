import React, { useState } from 'react';
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
  const [diaryData, setDiaryData] = useState({
    diary_id: 1,
    diary_date: "2026.05.07 목요일",
    diary_content:
      "오늘 프로젝트가 생각대로 잘 안 풀려서 조금 슬펐지만, 팀원들과 다시 처음부터 세팅을 맞추고 나니 마음이 한결 편안해졌다. 내일은 더 잘할 수 있겠지? 화이팅!",

    emotions: [
      { name: '행복', ratio: 75, color: 'bg-[#ffedd5]' },
      { name: '평범', ratio: 10, color: 'bg-[#fef08a]' },
      { name: '놀람', ratio: 5, color: 'bg-[#ccfbf1]' },
      { name: '슬픔', ratio: 10, color: 'bg-[#fbcfe8]' },
      { name: '분노', ratio: 0, color: 'bg-[#fca5a5]' },
      { name: '혐오', ratio: 0, color: 'bg-[#99f6e4]' },
    ]
  });

  const [placeRecommendation, setPlaceRecommendation] = useState({
    place_name: "조용한 카페 아늑",
    address: "경기 용인시 수지구 죽전로 152"
  });

  const [musicRecommendations, setMusicRecommendations] = useState([
    {
      music_recommendation_id: 1,
      title: "조용한 피아노 선율",
      artist: "InnerPeace",
      youtube_url: "#"
    },
    {
      music_recommendation_id: 2,
      title: "마음이 편안해지는 lofi",
      artist: "ChillHop",
      youtube_url: "#"
    }
  ]);

  const [missionRecommendation, setMissionRecommendation] = useState({
    mission_content:
      "오늘 하루 나에게 '고생했어'라고 한 마디 말해주기",
    mission_type: "자존감 회복"
  });

  return (
    <MobileLayout>
      {/* 상단 인디케이터 상태바 */}
      <div className="px-6 pt-3 flex justify-between items-center text-xs text-gray-500 bg-white font-medium">
        <span>9:41</span>

        <div className="flex items-center gap-1">
          <span>📶</span>
          <span>🔋</span>
        </div>
      </div>

      {/* 헤더 & 상단 탭 */}
      <header className="pt-4 pb-2 px-6 bg-white">
        <h1 className="text-xl font-bold text-center text-gray-900 tracking-tight">
          InnerNote
        </h1>

        <div className="flex gap-2 mt-4 border-b border-gray-100">
          <button className="pb-2 px-3 text-sm font-bold border-b-2 border-red-400 text-red-500">
            일별
          </button>

          <button className="pb-2 px-3 text-sm font-medium text-gray-400 hover:text-gray-600">
            주별
          </button>

          <button className="pb-2 px-3 text-sm font-medium text-gray-400 hover:text-gray-600">
            월별
          </button>
        </div>
      </header>

      {/* 메인 콘텐츠 */}
      <main className="flex-1 overflow-y-auto pb-24 bg-gray-50/50 px-5 pt-4">

        {/* 날짜 컨트롤러 */}
        <div className="flex justify-between items-center mb-5 px-2">
          <button className="p-1 rounded-full hover:bg-gray-200 transition">
            <ChevronLeft className="w-5 h-5 text-gray-600" />
          </button>

          <span className="text-sm font-semibold text-gray-700">
            {diaryData.diary_date}
          </span>

          <button className="p-1 rounded-full hover:bg-gray-200 transition">
            <ChevronRight className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* 감정 분석 카드 */}
        <div className="bg-white p-5 rounded-3xl shadow-sm border border-gray-100/80 mb-5">

          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center gap-1.5">
              <BarChart2 className="w-4 h-4 text-purple-500" />

              <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                Hugging Face 감정 분석
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between gap-4">

            <div className="relative w-36 h-36 rounded-full flex items-center justify-center emotion-chart shrink-0 shadow-sm">

              <div className="absolute w-22 h-22 bg-white rounded-full flex flex-col items-center justify-center shadow-inner">
                <span className="text-lg">🤍</span>

                <span className="font-extrabold text-gray-800 text-base">
                  행복
                </span>

                <span className="text-gray-500 font-bold text-xs">
                  75%
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-x-3 gap-y-2 flex-1 text-xs">
              {diaryData.emotions.map((emo, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-1.5 text-gray-600 font-medium"
                >
                  <span
                    className={`w-2.5 h-2.5 rounded-full ${emo.color} border border-gray-200/50`}
                  ></span>

                  <span
                    className={emo.ratio > 0
                      ? "font-bold text-gray-800"
                      : ""}
                  >
                    {emo.name} {emo.ratio > 0 && `${emo.ratio}%`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <h2 className="text-base font-bold text-gray-800 mb-3 px-1 flex items-center gap-1">
          ✨ 오늘의 맞춤형 추천
        </h2>

        <div className="space-y-4">

          <div className="grid grid-cols-2 gap-4">

            <div className="bg-blue-50/60 border border-blue-100 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]">

              <div className="flex items-center gap-1 text-blue-700 font-bold text-xs mb-2">
                <MapPin className="w-3.5 h-3.5" />
                <span>추천 장소</span>
              </div>

              <div>
                <p className="font-extrabold text-gray-800 text-sm leading-snug">
                  {placeRecommendation.place_name}
                </p>

                <p className="text-[11px] text-gray-500 mt-1 font-medium">
                  {placeRecommendation.address}
                </p>
              </div>
            </div>

            <div className="bg-purple-50/60 border border-purple-100 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]">

              <div className="flex items-center gap-1 text-purple-700 font-bold text-xs mb-2">
                <Music className="w-3.5 h-3.5" />
                <span>오늘의 음악</span>
              </div>

              <div className="space-y-2">
                {musicRecommendations.map((music) => (
                  <div
                    key={music.music_recommendation_id}
                    className="flex items-center gap-1.5 text-xs text-gray-700 group cursor-pointer hover:text-purple-700"
                  >
                    <Play className="w-3 h-3 text-gray-500 fill-gray-500 group-hover:text-purple-600 group-hover:fill-purple-600 shrink-0" />

                    <span className="truncate font-medium">
                      {music.title}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-emerald-50/60 border border-emerald-100 rounded-2xl p-4">

            <div className="flex items-center gap-1 text-emerald-700 font-bold text-xs mb-1.5">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>
                오늘의 미션 ({missionRecommendation.mission_type})
              </span>
            </div>

            <p className="text-xs text-gray-700 font-semibold leading-relaxed">
              "{missionRecommendation.mission_content}"
            </p>
          </div>
        </div>
      </main>
    </MobileLayout>
  );
}

export default StatisticsPage;