import React, { createContext, useContext, useReducer, useCallback, useMemo, useEffect } from 'react';
import { useApiClient } from '../hooks/useApiClient';

// Initial state
const initialState = {
  budgetAllocation: [],
  executionStatus: [],
  yearlyTrends: [],
  filters: {
    department: null,
    year: new Date().getFullYear(),
    budgetCategory: null,
    dateRange: {
      startDate: null,
      endDate: null,
    },
  },
  loadingState: {
    allocation: false,
    execution: false,
    trends: false,
  },
  error: null,
  selectedView: 'chart',
};

// Reducer
function budgetReducer(state, action) {
  switch (action.type) {
    case 'FETCH_INIT':
      return {
        ...state,
        loadingState: { allocation: true, execution: true, trends: true },
        error: null,
      };

    case 'FETCH_SUCCESS':
      return {
        ...state,
        budgetAllocation: action.payload.allocation ?? state.budgetAllocation,
        executionStatus: action.payload.execution ?? state.executionStatus,
        yearlyTrends: action.payload.trends ?? state.yearlyTrends,
        loadingState: { allocation: false, execution: false, trends: false },
        error: null,
      };

    case 'FETCH_ERROR':
      return {
        ...state,
        loadingState: { allocation: false, execution: false, trends: false },
        error: action.payload,
      };

    case 'UPDATE_FILTER':
      return {
        ...state,
        filters: { ...state.filters, ...action.payload },
      };

    case 'RESET_FILTERS':
      return {
        ...state,
        filters: initialState.filters,
      };

    case 'TOGGLE_VIEW':
      return {
        ...state,
        selectedView: action.payload,
      };

    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };

    default:
      return state;
  }
}

// Context
const BudgetContext = createContext(undefined);

// Provider
export function BudgetProvider({ children }) {
  const [state, dispatch] = useReducer(budgetReducer, initialState);
  const { apiClient } = useApiClient();

  // Fetch all budget data
  const fetchBudgetData = useCallback(async () => {
    dispatch({ type: 'FETCH_INIT' });

    try {
      const { filters } = state;

      // Build query params
      const params = new URLSearchParams();
      if (filters.department) params.append('department', filters.department);
      if (filters.year) params.append('year', filters.year.toString());
      if (filters.budgetCategory) params.append('category', filters.budgetCategory);
      if (filters.dateRange.startDate) params.append('start_date', filters.dateRange.startDate);
      if (filters.dateRange.endDate) params.append('end_date', filters.dateRange.endDate);

      const paramString = params.toString();

      // Parallel API calls
      const [allocationRes, executionRes, trendsRes] = await Promise.all([
        apiClient.get(`/budget/allocation/?${paramString}`),
        apiClient.get(`/budget/execution/?${paramString}`),
        apiClient.get(`/budget/trends/?${paramString}`),
      ]);

      dispatch({
        type: 'FETCH_SUCCESS',
        payload: {
          allocation: allocationRes.data.data || [],
          execution: executionRes.data.data || [],
          trends: trendsRes.data.data || [],
        },
      });
    } catch (error) {
      dispatch({
        type: 'FETCH_ERROR',
        payload: {
          type: error.response?.status === 401 ? 'auth' : 'network',
          message: error.response?.data?.error?.message || error.message || 'Failed to fetch budget data',
          details: error.response?.data?.error?.code,
        },
      });
    }
  }, [state.filters, apiClient]);

  // Auto-fetch on mount and filter changes
  useEffect(() => {
    fetchBudgetData();
  }, [state.filters]);

  // Computed values
  const overallExecutionRate = useMemo(() => {
    if (state.executionStatus.length === 0) return 0;
    const totalBudget = state.executionStatus.reduce((sum, item) => sum + (item.total_budget || 0), 0);
    const totalExecuted = state.executionStatus.reduce((sum, item) => sum + (item.executed_amount || 0), 0);
    return totalBudget > 0 ? (totalExecuted / totalBudget) * 100 : 0;
  }, [state.executionStatus]);

  const totalBudget = useMemo(() => {
    return state.budgetAllocation.reduce((sum, item) => sum + (item.total_budget || 0), 0);
  }, [state.budgetAllocation]);

  const totalExecuted = useMemo(() => {
    return state.executionStatus.reduce((sum, item) => sum + (item.executed_amount || 0), 0);
  }, [state.executionStatus]);

  const totalRemaining = useMemo(() => {
    return state.executionStatus.reduce((sum, item) => sum + (item.remaining_budget || 0), 0);
  }, [state.executionStatus]);

  const warningDepartments = useMemo(() => {
    return state.executionStatus.filter(item => item.status === 'warning').length;
  }, [state.executionStatus]);

  const criticalDepartments = useMemo(() => {
    return state.executionStatus.filter(item => item.status === 'critical').length;
  }, [state.executionStatus]);

  const isLoading = useMemo(() => {
    return state.loadingState.allocation || state.loadingState.execution || state.loadingState.trends;
  }, [state.loadingState]);

  // Action functions
  const updateFilter = useCallback((filter) => {
    dispatch({ type: 'UPDATE_FILTER', payload: filter });
  }, []);

  const resetFilters = useCallback(() => {
    dispatch({ type: 'RESET_FILTERS' });
  }, []);

  const toggleView = useCallback((view) => {
    dispatch({ type: 'TOGGLE_VIEW', payload: view });
  }, []);

  const retryFetch = useCallback(async () => {
    dispatch({ type: 'CLEAR_ERROR' });
    await fetchBudgetData();
  }, [fetchBudgetData]);

  const value = {
    state,
    overallExecutionRate,
    totalBudget,
    totalExecuted,
    totalRemaining,
    warningDepartments,
    criticalDepartments,
    isLoading,
    fetchBudgetData,
    updateFilter,
    resetFilters,
    toggleView,
    retryFetch,
  };

  return (
    <BudgetContext.Provider value={value}>
      {children}
    </BudgetContext.Provider>
  );
}

// Custom hook
export function useBudget() {
  const context = useContext(BudgetContext);

  if (context === undefined) {
    throw new Error('useBudget must be used within BudgetProvider');
  }

  return context;
}
