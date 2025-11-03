/**
 * Dashboard API Client
 * Handles all API calls related to dashboard data.
 * Follows the plan.md specifications.
 */

import { createAuthenticatedClient } from './client';

/**
 * Fetch complete dashboard data from backend.
 *
 * @param {string} token - JWT authentication token
 * @returns {Promise<Object>} Dashboard data with KPIs, trends, department data, and budget data
 * @throws {Error} API error with message, code, and statusCode
 */
export const fetchDashboardData = async (token) => {
  const client = createAuthenticatedClient(token);

  try {
    const response = await client.get('/dashboard/dashboard/');
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with an error
      const errorData = error.response.data.error || {};
      throw {
        message: errorData.message || 'Failed to fetch dashboard data',
        code: errorData.code || 'API_ERROR',
        statusCode: error.response.status
      };
    } else if (error.request) {
      // Request sent but no response received
      throw {
        message: 'Network error. Please check your connection.',
        code: 'NETWORK_ERROR',
        statusCode: 0
      };
    } else {
      // Request setup error
      throw {
        message: 'Failed to send request',
        code: 'REQUEST_ERROR',
        statusCode: 0
      };
    }
  }
};
