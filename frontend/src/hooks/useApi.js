import { useCallback, useState } from 'react';

const useApi = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const execute = useCallback(async (url, options = {}) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(url, options);
      const result = await response.json();

      if (!response.ok) {
        setError(result.detail || 'An error occurred');
        return null;
      }

      setData(result);
      return result;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Network error';
      setError(errorMsg);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, error, loading, execute };
};

export default useApi;
