/**
 * Axios API client configuration.
 * Following the common-modules.md specification.
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Create basic API client without authentication.
 * Used for public endpoints.
 */
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Create authenticated API client with Clerk token.
 * Used for protected endpoints that require authentication.
 *
 * @param {string} token - Clerk JWT token
 * @returns {AxiosInstance} Configured axios instance with authentication
 */
export const createAuthenticatedClient = (token) => {
  return axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    timeout: 10000,
  });
};

/**
 * Response interceptor for error handling.
 * Logs errors and provides consistent error handling.
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
      console.error('Status:', error.response.status);
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error:', error.message);
    } else {
      // Error in request configuration
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;
