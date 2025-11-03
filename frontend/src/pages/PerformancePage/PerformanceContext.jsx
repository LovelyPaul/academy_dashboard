import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import PropTypes from 'prop-types';
import { useApiClient } from '../../hooks/useApiClient';
import { fetchPerformanceData } from '../../api/performanceApi';

// Action Types
const ActionTypes = {
  FETCH_PERFORMANCE_REQUEST: 'FETCH_PERFORMANCE_REQUEST',
  FETCH_PERFORMANCE_SUCCESS: 'FETCH_PERFORMANCE_SUCCESS',
  FETCH_PERFORMANCE_FAILURE: 'FETCH_PERFORMANCE_FAILURE',
  UPDATE_FILTERS: 'UPDATE_FILTERS',
  RESET_FILTERS: 'RESET_FILTERS',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
};

// Date Helper Functions
const getDateOneYearAgo = () => {
  const date = new Date();
  date.setFullYear(date.getFullYear() - 1);
  return date.toISOString().split('T')[0]; // YYYY-MM-DD
};

const getTodayDate = () => {
  return new Date().toISOString().split('T')[0]; // YYYY-MM-DD
};

// Default Filter Values
const defaultFilters = {
  startDate: getDateOneYearAgo(),
  endDate: getTodayDate(),
  department: null,
  project: null,
};

// Initial State
const initialState = {
  performanceData: null,
  filters: defaultFilters,
  loadingState: {
    initial: true,
    filter: false,
  },
  error: null,
};

// Reducer Function
function performanceReducer(state, action) {
  switch (action.type) {
    case ActionTypes.FETCH_PERFORMANCE_REQUEST:
      return {
        ...state,
        loadingState: {
          initial: state.performanceData === null,
          filter: state.performanceData !== null,
        },
        error: null,
      };

    case ActionTypes.FETCH_PERFORMANCE_SUCCESS:
      return {
        ...state,
        performanceData: action.payload,
        loadingState: {
          initial: false,
          filter: false,
        },
        error: null,
      };

    case ActionTypes.FETCH_PERFORMANCE_FAILURE:
      return {
        ...state,
        loadingState: {
          initial: false,
          filter: false,
        },
        error: {
          type: action.payload.type,
          message: action.payload.message,
        },
      };

    case ActionTypes.UPDATE_FILTERS:
      return {
        ...state,
        filters: {
          ...state.filters,
          ...action.payload,
        },
      };

    case ActionTypes.RESET_FILTERS:
      return {
        ...state,
        filters: defaultFilters,
      };

    case ActionTypes.SET_ERROR:
      return {
        ...state,
        error: action.payload,
      };

    case ActionTypes.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };

    default:
      return state;
  }
}

// Error Type Detection
function getErrorType(error) {
  if (error.response?.status === 401) return 'auth';
  if (error.response?.status === 400) return 'validation';
  if (error.response?.status >= 500) return 'network';
  if (!error.response) return 'network';
  return 'data';
}

// Error Message Extraction
function getErrorMessage(error) {
  if (error.response?.data?.error?.message) {
    return error.response.data.error.message;
  }
  if (error.response?.status === 401) {
    return '인증이 만료되었습니다. 다시 로그인해주세요.';
  }
  if (error.response?.status === 400) {
    return '필터 조건이 올바르지 않습니다.';
  }
  if (!error.response) {
    return '네트워크 연결을 확인해주세요.';
  }
  return '데이터를 불러오는데 실패했습니다.';
}

// Create Context
const PerformanceContext = createContext(null);

// Context Provider Component
export function PerformanceProvider({ children }) {
  const [state, dispatch] = useReducer(performanceReducer, initialState);
  const { getAuthenticatedClient } = useApiClient();
  const [searchParams, setSearchParams] = useSearchParams();

  // Fetch Performance Data
  const fetchData = useCallback(async (filters) => {
    dispatch({ type: ActionTypes.FETCH_PERFORMANCE_REQUEST });

    try {
      const client = await getAuthenticatedClient();
      const data = await fetchPerformanceData(client, {
        startDate: filters.startDate,
        endDate: filters.endDate,
        department: filters.department,
        project: filters.project,
      });

      dispatch({
        type: ActionTypes.FETCH_PERFORMANCE_SUCCESS,
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: ActionTypes.FETCH_PERFORMANCE_FAILURE,
        payload: {
          type: getErrorType(error),
          message: getErrorMessage(error),
        },
      });
    }
  }, [getAuthenticatedClient]);

  // Update URL Parameters
  const updateUrlParams = useCallback((filters) => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.set(key, value);
      }
    });

    setSearchParams(params);
  }, [setSearchParams]);

  // Action Creators
  const actions = {
    fetchPerformanceData: fetchData,

    updateFilters: (newFilters) => {
      // 1. Update filter state
      dispatch({
        type: ActionTypes.UPDATE_FILTERS,
        payload: newFilters,
      });

      // 2. Update URL parameters
      updateUrlParams({ ...state.filters, ...newFilters });
    },

    resetFilters: () => {
      dispatch({ type: ActionTypes.RESET_FILTERS });
      setSearchParams({});
    },

    clearError: () => {
      dispatch({ type: ActionTypes.CLEAR_ERROR });
    },
  };

  // Initialize from URL parameters on mount
  useEffect(() => {
    const startDate = searchParams.get('startDate');
    const endDate = searchParams.get('endDate');
    const department = searchParams.get('department');
    const project = searchParams.get('project');

    if (startDate || endDate || department || project) {
      const urlFilters = {
        startDate: startDate || defaultFilters.startDate,
        endDate: endDate || defaultFilters.endDate,
        department: department || null,
        project: project || null,
      };

      dispatch({
        type: ActionTypes.UPDATE_FILTERS,
        payload: urlFilters,
      });
    }
  }, []); // Run only once on mount

  // Fetch data when filters change
  useEffect(() => {
    if (!state.loadingState.initial) {
      fetchData(state.filters);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.filters.startDate, state.filters.endDate, state.filters.department, state.filters.project]);

  // Initial data fetch
  useEffect(() => {
    if (state.loadingState.initial) {
      fetchData(state.filters);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = {
    state,
    actions,
    dispatch,
  };

  return (
    <PerformanceContext.Provider value={value}>
      {children}
    </PerformanceContext.Provider>
  );
}

PerformanceProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

// Custom Hook to use Performance Context
export function usePerformanceContext() {
  const context = useContext(PerformanceContext);

  if (!context) {
    throw new Error('usePerformanceContext must be used within PerformanceProvider');
  }

  return context;
}
