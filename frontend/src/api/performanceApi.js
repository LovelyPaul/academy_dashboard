/**
 * Performance API client
 *
 * Provides functions to interact with performance endpoints
 */

/**
 * Fetch performance data with filters
 *
 * @param {Object} client - Authenticated axios client
 * @param {Object} filters - Filter parameters
 * @param {string} filters.startDate - Start date (YYYY-MM-DD)
 * @param {string} filters.endDate - End date (YYYY-MM-DD)
 * @param {string} [filters.department] - Department filter
 * @param {string} [filters.project] - Project filter
 * @returns {Promise<Object>} Performance data
 */
export const fetchPerformanceData = async (client, filters = {}) => {
  const params = new URLSearchParams();

  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);
  if (filters.department) params.append('department', filters.department);
  if (filters.project) params.append('project', filters.project);

  const queryString = params.toString();
  const url = queryString ? `/performance/?${queryString}` : '/performance/';

  const response = await client.get(url);
  return response.data;
};

/**
 * Fetch available departments for filter options
 *
 * @param {Object} client - Authenticated axios client
 * @returns {Promise<Array>} List of departments
 */
export const fetchDepartments = async (client) => {
  // This would ideally be a separate endpoint
  // For now, we'll return empty array (to be implemented later)
  // In production, this should call GET /departments/
  return [];
};

/**
 * Fetch available projects for filter options
 *
 * @param {Object} client - Authenticated axios client
 * @returns {Promise<Array>} List of projects
 */
export const fetchProjects = async (client) => {
  // This would ideally be a separate endpoint
  // For now, we'll return empty array (to be implemented later)
  // In production, this should call GET /projects/
  return [];
};
