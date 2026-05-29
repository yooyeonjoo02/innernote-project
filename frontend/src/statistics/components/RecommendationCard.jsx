import React from 'react';

import {
  Play,
  MapPin,
  Music,
  CheckCircle
} from 'lucide-react';

function getYoutubeThumbnailUrl(url) {
  if (!url) return null;

  const videoId = url.split('v=')[1]?.split('&')[0];

  if (!videoId) return null;

  return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
}

function RecommendationCard({ recommendation }) {
  if (!recommendation) return null;

  const {
    music,
    place,
    mission,
    recommendation_type
  } = recommendation;

  const thumbnailUrl =
    music?.thumbnail_url ||
    music?.thumbnailUrl ||
    getYoutubeThumbnailUrl(music?.url);

  const missionText =
    typeof mission === 'string'
      ? mission
      : mission?.content ||
        mission?.description ||
        mission?.text ||
        mission?.title ||
        '오늘의 미션이 없습니다.';

  return (
    <>
      <h2 className="text-base font-bold text-gray-800 mb-3 px-1 flex items-center gap-1">
        ✨ 오늘의 맞춤형 추천
      </h2>

      <p className="text-[11px] text-gray-500 mb-3 px-1">
        {recommendation_type === 'comfort'
          ? '오늘은 익숙하고 좋아하는 것들로 마음을 쉬어가요.'
          : '오늘은 새로운 경험을 해보는 건 어때요?'}
      </p>

      <div className="grid grid-cols-2 gap-4">
        <a
          href={place?.url || '#'}
          target={place?.url ? '_blank' : '_self'}
          rel="noreferrer"
          className="bg-white shadow-sm border border-blue-100/30 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]"
        >
          <div className="flex items-center gap-1 text-blue-700 font-bold text-xs mb-2">
            <MapPin className="w-3.5 h-3.5" />
            <span>추천 장소</span>
          </div>

          <div>
            <p className="font-extrabold text-gray-800 text-sm leading-snug">
              {place?.name || '추천 장소 없음'}
            </p>

            <p className="text-[11px] text-gray-500 mt-1 font-medium">
              {place?.address || ''}
            </p>
          </div>
        </a>

        <a
          href={music?.url || '#'}
          target={music?.url ? '_blank' : '_self'}
          rel="noreferrer"
          className="bg-white shadow-sm border border-purple-100/30 rounded-2xl p-4 flex flex-col justify-between min-h-[140px]"
        >
          <div className="flex items-center gap-1 text-purple-700 font-bold text-xs mb-2">
            <Music className="w-3.5 h-3.5" />
            <span>오늘의 음악</span>
          </div>

          {thumbnailUrl && (
            <img
              src={thumbnailUrl}
              alt={music?.title || '유튜브 썸네일'}
              className="w-full h-[62px] object-cover rounded-xl mb-2 bg-gray-100"
            />
          )}

          <div className="flex items-center gap-1.5 text-xs text-gray-700 group cursor-pointer">
            <Play className="w-3 h-3 text-gray-500 fill-gray-500 shrink-0" />

            <span className="truncate font-medium">
              {music?.title || '추천 음악 없음'}
            </span>
          </div>
        </a>

        <div className="col-span-2 bg-white shadow-sm border border-orange-100/40 rounded-2xl p-4 min-h-[100px]">
          <div className="flex items-center gap-1 text-orange-500 font-bold text-xs mb-3">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>오늘의 미션</span>
          </div>

          <p className="font-semibold text-gray-800 text-sm leading-relaxed">
            {missionText}
          </p>
        </div>
      </div>
    </>
  );
}

export default RecommendationCard;