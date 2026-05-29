import React from 'react';

import { getEmotionBgClass } from '../utils/emotionUtils';

function EmotionLegend({ emotionsList }) {
  return (
    <div className="grid grid-cols-2 gap-x-3 gap-y-2 flex-1 text-xs">
      {emotionsList.map((emotion, index) => (
        <div
          key={index}
          className="flex items-center gap-1.5 text-gray-600 font-medium"
        >
          <span
            className={`w-2.5 h-2.5 rounded-full ${getEmotionBgClass(
              emotion.emotion_name
            )} border border-gray-200/50`}
          />

          <span
            className={
              emotion.ratio > 0
                ? 'font-bold text-gray-800'
                : ''
            }
          >
            {emotion.emotion_name}{' '}
            {emotion.ratio > 0 && `${emotion.ratio}%`}
          </span>
        </div>
      ))}
    </div>
  );
}

export default EmotionLegend;