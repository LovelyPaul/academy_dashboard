/**
 * Papers Context Provider
 *
 * Manages state and data fetching for Papers Analysis page.
 * Provides context with reducer pattern for state management.
 */

import React, { createContext, useReducer, useCallback, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApiClient } from '../../hooks/useApiClient';
import { useAuth } from '../../hooks/useAuth';
import {
  papersReducer,
  initialState,
  FETCH_PAPERS_START,
  FETCH_PAPERS_SUCCESS,
  FETCH_PAPERS_ERROR,
  SET_FILTER,
  CLEAR_FILTERS,
  RESET_ERROR
} from './papersReducer';

// Create context
export const PapersContext = createContext();

/**
 * Papers Provider Component
 *
 * Wraps children with context provider for papers analytics data.
 */
export function PapersProvider({ children }) {
  const [state, dispatch] = useReducer(papersReducer, initialState);
  const { getAuthenticatedClient } = useApiClient();
  const { getToken, signOut } = useAuth();
  const navigate = useNavigate();

  /**
   * Fetch papers analytics data from API
   */
  const fetchPapersData = useCallback(async () => {
    dispatch({ type: FETCH_PAPERS_START });

    try {
      const token = await getToken();
      const client = await getAuthenticatedClient();

      // Build query parameters
      const params = {};
      if (state.filters.year) params.year = state.filters.year;
      if (state.filters.journal) params.journal = state.filters.journal;
      if (state.filters.field) params.field = state.filters.field;

      // Make API request
      const response = await client.get('/papers/analytics/', { params });

      dispatch({
        type: FETCH_PAPERS_SUCCESS,
        payload: response.data
      });
    } catch (error) {
      // Handle authentication errors
      if (error.response?.status === 401) {
        dispatch({
          type: FETCH_PAPERS_ERROR,
          payload: {
            message: 'Session expired. Please login again.',
            code: '401'
          }
        });
        signOut();
        navigate('/sign-in');
      } else {
        dispatch({
          type: FETCH_PAPERS_ERROR,
          payload: {
            message: error.response?.data?.error || 'Failed to load papers data',
            code: error.response?.status?.toString() || 'NETWORK_ERROR'
          }
        });
      }
    }
  }, [getToken, getAuthenticatedClient, state.filters, signOut, navigate]);

  /**
   * Set a single filter value
   *
   * @param {string} filterType - Type of filter (year, journal, field)
   * @param {any} value - Filter value
   */
  const setFilter = useCallback((filterType, value) => {
    dispatch({
      type: SET_FILTER,
      payload: { filterType, value }
    });
  }, []);

  /**
   * Clear all filters
   */
  const clearFilters = useCallback(() => {
    dispatch({ type: CLEAR_FILTERS });
  }, []);

  /**
   * Reset error state
   */
  const resetError = useCallback(() => {
    dispatch({ type: RESET_ERROR });
  }, []);

  /**
   * Refetch data when filters change
   */
  useEffect(() => {
    fetchPapersData();
  }, [state.filters]);

  /**
   * Memoize context value to prevent unnecessary re-renders
   */
  const contextValue = useMemo(() => ({
    state,
    dispatch,
    setFilter,
    clearFilters,
    resetError,
    refetchData: fetchPapersData
  }), [state, setFilter, clearFilters, resetError, fetchPapersData]);

  return (
    <PapersContext.Provider value={contextValue}>
      {children}
    </PapersContext.Provider>
  );
}

/**
 * Custom hook to use Papers context
 *
 * @returns {Object} Context value with state and actions
 * @throws {Error} If used outside PapersProvider
 */
export function usePapersContext() {
  const context = React.useContext(PapersContext);
  if (!context) {
    throw new Error('usePapersContext must be used within PapersProvider');
  }
  return context;
}
