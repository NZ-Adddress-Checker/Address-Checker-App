const apiClient = {
  getBaseUrl: () => {
    return import.meta.env.VITE_API_URL || 'http://localhost:8000';
  },

  get: async (endpoint, options = {}) => {
    const url = `${apiClient.getBaseUrl()}${endpoint}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }

    return response.json();
  },

  post: async (endpoint, body, options = {}) => {
    const url = `${apiClient.getBaseUrl()}${endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: JSON.stringify(body),
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'API request failed');
    }

    return data;
  },

  put: async (endpoint, body, options = {}) => {
    const url = `${apiClient.getBaseUrl()}${endpoint}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: JSON.stringify(body),
      ...options,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }

    return response.json();
  },

  delete: async (endpoint, options = {}) => {
    const url = `${apiClient.getBaseUrl()}${endpoint}`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }

    return response.json();
  },
};

export default apiClient;
