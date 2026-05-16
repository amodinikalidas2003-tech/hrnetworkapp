import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for API responses to handle standard ApiResponse format
apiClient.interceptors.response.use(
  (response) => {
    // Unpack the custom ApiResponse structure
    const data = response.data;
    if (data && data.success !== undefined) {
      if (data.success) {
        return data.data;
      } else {
        return Promise.reject(data.error);
      }
    }
    return response.data;
  },
  (error) => {
    // Handle global errors here (e.g., redirect to login on 401)
    return Promise.reject(error.response?.data?.error || error.message);
  }
);

export default apiClient;
