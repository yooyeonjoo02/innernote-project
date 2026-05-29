import React from 'react';

import {
  Play,
  MapPin,
  Music,
  CheckCircle
} from 'lucide-react';

function RecommendationCard({ recs }) {
  return (
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
              <p className="font-extrabold text-gray-800 text-sm leading-snug">
                {recs.place?.place_name}
              </p>

              <p className="text-[11px] text-gray-500 mt-1 font-medium">
                {recs.place?.address}
              </p>
            </div>
          </div>

          <div className="bg-white shadow-sm border border-purple-100/30 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]">
            <div className="flex items-center gap-1 text-purple-700 font-bold text-xs mb-2">
              <Music className="w-3.5 h-3.5" />
              <span>오늘의 음악</span>
            </div>

            <div className="space-y-2">
              {(recs.playlist || []).map((music) => (
                <a
                  href={music.youtube_url}
                  target="_blank"
                  rel="noreferrer"
                  key={music.music_id}
                  className="flex items-center gap-1.5 text-xs text-gray-700 group cursor-pointer block"
                >
                  <Play className="w-3 h-3 text-gray-500 fill-gray-500 group-hover:text-purple-600 group-hover:fill-purple-600 shrink-0" />

                  <span className="truncate font-medium group-hover:text-purple-600">
                    {music.title}
                  </span>
                </a>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white shadow-sm border border-emerald-100/30 rounded-2xl p-4">
          <div className="flex items-center gap-1 text-emerald-700 font-bold text-xs mb-1.5">
            <CheckCircle className="w-3.5 h-3.5" />

            <span>
              오늘의 미션 ({recs.mission?.mission_type})
            </span>
          </div>

          <p className="text-xs text-gray-700 font-semibold leading-relaxed">
            "{recs.mission?.mission_content}"
          </p>
        </div>
      </div>
    </>
  );
}

export default RecommendationCard;