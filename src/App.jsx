import { useState } from 'react';
// lucide-react: 하단 탭바 아이콘 (나침반, 홈, 프로필)
import { Compass, Home, User } from 'lucide-react';

// 설문 질문 목록: id(질문 번호), label(질문 텍스트), maxLength(DB VARCHAR 길이에 맞춘 글자 제한)
const questions = [
  { id: 1, label: '좋아하는 가수',                  maxLength: 50 }, // VARCHAR(50)
  { id: 2, label: '좋아하는 장르',                  maxLength: 30 }, // VARCHAR(30)
  { id: 3, label: '거주지(00구)',                   maxLength: 30 }, // VARCHAR(30)
  { id: 4, label: '좋아하는 장소(예시:노래방, 책방)', maxLength: 50 }, // VARCHAR(50)
  { id: 5, label: '가보고 싶은 장소',               maxLength: 50 }, // VARCHAR(50)
];

// 헤더 중앙에 표시되는 클립보드 SVG 아이콘
function ClipboardIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#333" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      {/* 클립보드 상단 클립 영역 */}
      <rect x="9" y="2" width="6" height="4" rx="1" />
      {/* 클립보드 본체 */}
      <path d="M9 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-2" />
      {/* 내부 첫 번째 줄 */}
      <line x1="9" y1="12" x2="15" y2="12" />
      {/* 내부 두 번째 줄 */}
      <line x1="9" y1="16" x2="13" y2="16" />
    </svg>
  );
}


function App() {
  // 각 질문의 답변 상태: { 질문id: 입력값 } 형태로 관리
  const [answers, setAnswers] = useState({ 1: '', 2: '', 3: '', 4: '', 5: '' });
  // 현재 포커스된 입력창의 질문 id (포커스 시 파란 테두리 표시에 사용)
  const [focused, setFocused] = useState(null);

  // 입력값 변경 핸들러: DB maxLength 초과 시 입력 차단
  const handleChange = (id, value, maxLength) => {
    if (value.length > maxLength) return;
    setAnswers((prev) => ({ ...prev, [id]: value }));
  };

  // 저장 버튼 클릭 핸들러
  const handleSave = () => {
    alert('저장되었습니다!');
  };

  return (
    // 전체 페이지 컨테이너 (375px 고정 너비, 모바일 화면 크기 모방)
    <div style={styles.page}>

      {/* 헤더: 좌측 행복 이모지 / 중앙 클립보드 아이콘 + 타이틀 / 우측 슬픔 이모지 */}
      <div style={styles.header}>
        <span style={styles.emoji}>😊</span>
        <div style={styles.headerCenter}>
          <ClipboardIcon />
          <span style={styles.headerTitle}>설문</span>
        </div>
        <span style={styles.emoji}>😞</span>
      </div>

      {/* 서브타이틀 */}
      <p style={styles.subtitle}>당신을 잘 알기 위한 질문들 이에요</p>

      {/* 질문 목록: questions 배열을 순회하며 질문 블록 렌더링 */}
      <div style={styles.questionList}>
        {questions.map((q) => (
          <div key={q.id} style={styles.questionBlock}>
            {/* 질문 번호 + 텍스트 레이블 */}
            <label style={styles.questionLabel}>
              {q.id}. {q.label}
            </label>
            {/* 입력창 + 문제 번호 표시를 relative/absolute로 겹쳐서 배치 */}
            <div style={styles.inputWrapper}>
              <textarea
                style={{
                  ...styles.textarea,
                  // 포커스 상태면 파란 테두리, 아니면 투명 테두리 (레이아웃 유지)
                  border: focused === q.id ? '2px solid #2196F3' : '2px solid transparent',
                }}
                value={answers[q.id]}
                onChange={(e) => handleChange(q.id, e.target.value, q.maxLength)}
                onFocus={() => setFocused(q.id)}
                onBlur={() => setFocused(null)}
                maxLength={q.maxLength}
              />
              {/* 현재 문제 번호 / 전체 문제 수 (입력창 우측 하단 고정) */}
              <span style={styles.questionCount}>
                {q.id}/{questions.length}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* 저장 버튼 */}
      <button style={styles.saveButton} onClick={handleSave}>
        저장
      </button>

      {/* 하단 탭바: 나침반(탐색) / 홈(현재 페이지, 강조) / 프로필 */}
      <div style={styles.tabBar}>
        <button style={styles.tabItem}><Compass size={22} color="#9ca3af" /></button>
        <button style={styles.tabItem}><Home size={24} color="#111827" fill="#111827" /></button>
        <button style={styles.tabItem}><User size={22} color="#9ca3af" /></button>
      </div>
    </div>
  );
}

// 인라인 스타일 객체
const styles = {
  // 전체 페이지: 375px 고정 너비, 연한 초록 배경
  page: {
    width: 375,
    minHeight: 1325,
    backgroundColor: '#b8d9a0',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    paddingLeft: 12,
    paddingRight: 12,
    paddingTop: 32,
    paddingBottom: 0,
    boxSizing: 'border-box',
    fontFamily: 'sans-serif',
    position: 'relative',
  },
  // 헤더 행: 양 끝 이모지 + 중앙 타이틀을 space-between으로 배치
  header: {
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  // 헤더 중앙: 아이콘과 텍스트를 가로로 정렬
  headerCenter: {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 700,
    color: '#222',
  },
  emoji: {
    fontSize: 22,
  },
  subtitle: {
    fontSize: 12,
    color: '#444',
    textAlign: 'center',
    marginTop: 6,
    marginBottom: 32,
  },
  // 질문 목록: 세로 방향 flex, 질문 간 24px 간격
  questionList: {
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    gap: 24,
  },
  // 개별 질문 블록: 레이블 + 입력창을 세로로 묶음
  questionBlock: {
    display: 'flex',
    flexDirection: 'column',
    gap: 6,
  },
  questionLabel: {
    fontSize: 14,
    fontWeight: 600,
    color: '#222',
    textAlign: 'left',
  },
  // 입력창 래퍼: 문제 번호를 absolute로 올리기 위해 relative 설정
  inputWrapper: {
    position: 'relative',
    width: 351,
  },
  // 텍스트 입력창: 흰색 둥근 박스, resize 비활성화
  textarea: {
    width: 351,
    height: 160,
    borderRadius: 16,
    backgroundColor: '#fff',
    resize: 'none',
    padding: '12px 14px',
    fontSize: 14,
    color: '#333',
    outline: 'none', // 브라우저 기본 포커스 링 제거 (커스텀 border로 대체)
    boxSizing: 'border-box',
    fontFamily: 'sans-serif',
  },
  // 문제 번호 표시: 입력창 우측 하단에 절대 위치로 고정
  questionCount: {
    position: 'absolute',
    bottom: 10,
    right: 14,
    fontSize: 11,
    color: '#aaa',
  },
  // 저장 버튼: 초록색 배경, 둥근 모서리
  saveButton: {
    marginTop: 28,
    width: 351,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#4caf50',
    color: '#fff',
    fontSize: 15,
    fontWeight: 700,
    border: 'none',
    cursor: 'pointer',
  },
  // 하단 탭바: 흰색 배경, 상단 구분선, sticky로 화면 하단에 고정
  tabBar: {
    marginTop: 'auto',
    width: 375,
    height: 60,
    backgroundColor: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-around',
    borderTop: '1px solid #e0e0e0',
    position: 'sticky',
    bottom: 0,
  },
  tabItem: {
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 8,
  },
};

export default App;
