import { useState, useEffect } from 'react';
import MobileLayout from '../../shared/components/MobileLayout';

const API_BASE = 'http://localhost:8000';

const questions = [
  { id: 1, key: 'favorite_singer', label: '좋아하는 가수', maxLength: 50 },
  { id: 2, key: 'favorite_genre', label: '좋아하는 장르', maxLength: 30 },
  { id: 3, key: 'residence_area', label: '거주지(00구)', maxLength: 30 },
  { id: 4, key: 'favorite_place', label: '좋아하는 장소(예시:노래방, 책방)', maxLength: 50 },
  { id: 5, key: 'want_to_go_place', label: '가보고 싶은 장소', maxLength: 50 },
];

const defaultAnswers = {
  favorite_singer: '',
  favorite_genre: '',
  residence_area: '',
  favorite_place: '',
  want_to_go_place: '',
};

function ClipboardIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#333" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="2" width="6" height="4" rx="1" />
      <path d="M9 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-2" />
      <line x1="9" y1="12" x2="15" y2="12" />
      <line x1="9" y1="16" x2="13" y2="16" />
    </svg>
  );
}

function SurveyPage() {
  const [answers, setAnswers] = useState(defaultAnswers);
  const [focused, setFocused] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetch(`${API_BASE}/api/surveys/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) return null;
        return res.json();
      })
      .then((data) => {
        if (data) {
          setAnswers({
            favorite_singer: data.favorite_singer || '',
            favorite_genre: data.favorite_genre || '',
            residence_area: data.residence_area || '',
            favorite_place: data.favorite_place || '',
            want_to_go_place: data.want_to_go_place || '',
          });
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [token]);

  const handleChange = (key, value, maxLength) => {
    if (value.length > maxLength) return;
    setAnswers((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    if (!token) {
      alert('로그인이 필요합니다.');
      return;
    }

    setSaving(true);
    try {
      const res = await fetch(`${API_BASE}/api/surveys`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(answers),
      });

      if (!res.ok) throw new Error();
      alert('저장되었습니다!');
    } catch {
      alert('저장에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <MobileLayout>
        <div style={{ ...styles.page, justifyContent: 'center' }}>
          <p style={{ color: '#444' }}>불러오는 중...</p>
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout>
      <div style={styles.page}>
        <div style={styles.header}>
          <span style={styles.emoji}>😊</span>

          <div style={styles.headerCenter}>
            <ClipboardIcon />
            <span style={styles.headerTitle}>설문</span>
          </div>

          <span style={styles.emoji}>😞</span>
        </div>

        <p style={styles.subtitle}>당신을 잘 알기 위한 질문들 이에요</p>

        <div style={styles.questionList}>
          {questions.map((q) => (
            <div key={q.id} style={styles.questionBlock}>
              <label style={styles.questionLabel}>
                {q.id}. {q.label}
              </label>

              <div style={styles.inputWrapper}>
                <textarea
                  style={{
                    ...styles.textarea,
                    border: focused === q.id ? '2px solid #2196F3' : '2px solid transparent',
                  }}
                  value={answers[q.key]}
                  onChange={(e) => handleChange(q.key, e.target.value, q.maxLength)}
                  onFocus={() => setFocused(q.id)}
                  onBlur={() => setFocused(null)}
                  maxLength={q.maxLength}
                />

                <span style={styles.questionCount}>
                  {q.id}/{questions.length}
                </span>
              </div>
            </div>
          ))}
        </div>

        <button style={styles.saveButton} onClick={handleSave} disabled={saving}>
          {saving ? '저장 중...' : '저장'}
        </button>
      </div>
    </MobileLayout>
  );
}

const styles = {
  page: {
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
  },

  header: {
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
  },

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

  questionList: {
    width: 351,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: 24,
    margin: '0 auto',
  },

  questionBlock: {
    width: '100%',
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

  inputWrapper: {
    position: 'relative',
    width: '100%',
  },

  textarea: {
    width: '100%',
    height: 160,
    borderRadius: 16,
    backgroundColor: '#fff',
    resize: 'none',
    padding: '12px 14px',
    fontSize: 14,
    color: '#333',
    outline: 'none',
    boxSizing: 'border-box',
    fontFamily: 'sans-serif',
  },

  questionCount: {
    position: 'absolute',
    bottom: 10,
    right: 14,
    fontSize: 11,
    color: '#aaa',
  },

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
};

export default SurveyPage;
