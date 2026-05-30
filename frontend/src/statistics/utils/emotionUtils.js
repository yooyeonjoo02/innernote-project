export const emotionColorMap = {
  공포: '#ddd6fe',
  놀람: '#ccfbf1',
  분노: '#fca5a5',
  슬픔: '#fbcfe8',
  중립: '#fef08a',
  행복: '#ffedd5',
  혐오: '#99f6e4'
};

export const getEmotionBgClass = (name) => {
  const classes = {
    공포: 'bg-[#ddd6fe]',
    놀람: 'bg-[#ccfbf1]',
    분노: 'bg-[#fca5a5]',
    슬픔: 'bg-[#fbcfe8]',
    중립: 'bg-[#fef08a]',
    행복: 'bg-[#ffedd5]',
    혐오: 'bg-[#99f6e4]'
  };

  return classes[name] || 'bg-gray-200';
};

export const getEmotionEmoji = (name) => {
  const emojis = {
    공포: '😨',
    놀람: '😲',
    분노: '😡',
    슬픔: '😢',
    중립: '😐',
    행복: '😊',
    혐오: '🤢'
  };

  return emojis[name] || '🤍';
};