/**
 * Dashboard Context Provider
 * State management for dashboard page using useReducer (Flux pattern).
 * Follows the state.md specifications.
 */

import { createContext, useContext, useReducer, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { fetchDashboardData } from '../api/dashboardApi';

// Action Types
const ActionTypes = {
  FETCH_DASHBOARD_START: 'FETCH_DASHBOARD_START',
  FETCH_DASHBOARD_SUCCESS: 'FETCH_DASHBOARD_SUCCESS',
  FETCH_DASHBOARD_FAILURE: 'FETCH_DASHBOARD_FAILURE',
  CLEAR_ERROR: 'CLEAR_ERROR',
};

// Initial State
const initialState = {
  kpiData: null,
  trendData: [],
  departmentData: [],
  budgetData: [],
  isLoading: true,
  error: null,
  lastUpdated: null,
};

// Reducer Function
function dashboardReducer(state, action) {
  switch (action.type) {
    case ActionTypes.FETCH_DASHBOARD_START:
      return {
        ...state,
        isLoading: true,
        error: null,
      };

    case ActionTypes.FETCH_DASHBOARD_SUCCESS:
      return {
        ...state,
        kpiData: action.payload.kpi_data || action.payload.kpiData,
        trendData: action.payload.trend_data || action.payload.trendData,
        departmentData: action.payload.department_data || action.payload.departmentData,
        budgetData: action.payload.budget_data || action.payload.budgetData,
        lastUpdated: action.payload.last_updated || action.payload.lastUpdated,
        isLoading: false,
        error: null,
      };

    case ActionTypes.FETCH_DASHBOARD_FAILURE:
      return {
        ...state,
        isLoading: false,
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

// Context
const DashboardContext = createContext();

/**
 * Dashboard Provider Component
 * Manages dashboard state and provides data to child components.
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 */
export const DashboardProvider = ({ children }) => {
  const [state, dispatch] = useReducer(dashboardReducer, initialState);
  const { getToken, signOut } = useAuth();

  /**
   * Fetch dashboard data from API
   */
  const fetchData = async () => {
    dispatch({ type: ActionTypes.FETCH_DASHBOARD_START });

    try {
      const token = await getToken();
      const data = await fetchDashboardData(token);

      dispatch({
        type: ActionTypes.FETCH_DASHBOARD_SUCCESS,
        payload: data,
      });
    } catch (error) {
      // Handle token expiration (401 Unauthorized)
      if (error.statusCode === 401) {
        signOut();
        return;
      }

      dispatch({
        type: ActionTypes.FETCH_DASHBOARD_FAILURE,
        payload: error,
      });
    }
  };

  /**
   * Refresh dashboard data
   * Same as fetchData but can be called manually
   */
  const refreshDashboard = async () => {
    await fetchData();
  };

  /**
   * Clear error state
   */
  const clearError = () => {
    dispatch({ type: ActionTypes.CLEAR_ERROR });
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchData();
  }, []);

  // Context value
  const value = {
    // State
    ...state,

    // Actions
    fetchDashboardData: fetchData,
    refreshDashboard,
    clearError,
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
};

/**
 * Custom Hook to use Dashboard Context
 * Throws error if used outside DashboardProvider.
 *
 * @returns {Object} Dashboard context value
 * @throws {Error} If used outside DashboardProvider
 */
export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within DashboardProvider');
  }
  return context;
};
