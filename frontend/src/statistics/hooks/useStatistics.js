import { useEffect, useState } from 'react';

function useStatistics(selectedDate, viewType) {
  const [statData, setStatData] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recommendationLoading, setRecommendationLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recommendationError, setRecommendationError] = useState(null);

  useEffect(() => {
    const fetchStatistics = async () => {
      setLoading(true);
      setError(null);

      try {
        let url = '';

        if (viewType === 'daily') {
          url = `/api/v1/statistics/daily?date=${selectedDate}`;
        }

        if (viewType === 'weekly') {
          url = `/api/v1/statistics/weekly?date=${selectedDate}`;
        }

        if (viewType === 'monthly') {
          url = `/api/v1/statistics/monthly?date=${selectedDate}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error('통계 서버 통신 실패');
        }

        const result = await response.json();

        if (result.status === 'success') {
          setStatData(result.data);
        } else {
          setStatData(null);
        }
      } catch (err) {
        setError(err.message);
        setStatData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchStatistics();
  }, [selectedDate, viewType]);

  useEffect(() => {
    const fetchRecommendation = async () => {
      if (viewType !== 'daily') {
        setRecommendation(null);
        return;
      }

      setRecommendationLoading(true);
      setRecommendationError(null);

      try {
        const token =
          localStorage.getItem('accessToken') ||
          localStorage.getItem('access_token') ||
          localStorage.getItem('token');

        if (!token) {
          throw new Error('로그인 토큰이 없습니다.');
        }

        const response = await fetch(
          `/api/recommendations/daily?target_date=${selectedDate}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        if (!response.ok) {
          throw new Error('추천 서버 통신 실패');
        }

        const result = await response.json();
        setRecommendation(result);
      } catch (err) {
        setRecommendationError(err.message);
        setRecommendation(null);
      } finally {
        setRecommendationLoading(false);
      }
    };

    fetchRecommendation();
  }, [selectedDate, viewType]);

  return {
    statData,
    recommendation,
    loading,
    recommendationLoading,
    error,
    recommendationError
  };
}

export default useStatistics;