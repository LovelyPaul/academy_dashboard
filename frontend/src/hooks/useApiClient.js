/**
 * API client hook with authentication.
 * Following the common-modules.md specification.
 */
import { useAuth } from './useAuth';
import { createAuthenticatedClient, apiClient } from '../api/client';

/**
 * Custom hook to provide authenticated API client.
 * Manages authentication token injection into API requests.
 *
 * @returns {Object} API clients
 * @returns {Function} getAuthenticatedClient - Async function to get authenticated client
 * @returns {AxiosInstance} publicClient - Public API client without authentication
 */
export const useApiClient = () => {
  const { getToken } = useAuth();

  /**
   * Get authenticated API client with current user's token.
   * Call this before making authenticated API requests.
   *
   * @returns {Promise<AxiosInstance>} Authenticated axios instance
   */
  const getAuthenticatedClient = async () => {
    const token = await getToken();
    return createAuthenticatedClient(token);
  };

  return {
    getAuthenticatedClient,
    publicClient: apiClient,
  };
};

export default useApiClient;
