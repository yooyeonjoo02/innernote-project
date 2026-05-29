import { useEffect, useState } from 'react';

function useStatistics(selectedDate, viewType) {
  const [statData, setStatData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
          throw new Error('백엔드 서버 통신 실패');
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

  return {
    statData,
    loading,
    error
  };
}

export default useStatistics;