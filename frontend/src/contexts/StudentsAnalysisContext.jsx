/**
 * StudentsAnalysisProvider: State management using Context + useReducer pattern
 * Manages all state and logic for the Students Analysis page
 * Following the state.md design specification
 */
import React, { createContext, useReducer, useContext, useEffect, useMemo, useCallback } from 'react';
import { useApiClient } from '../hooks/useApiClient';

// Initial state
const initialState = {
  departmentStats: [],
  gradeDistribution: [],
  enrollmentTrend: [],
  loading: true,
  error: null,
  chartLoadingStatus: {
    department: false,
    grade: false,
    trend: false,
  },
  selectedDepartment: null,
  selectedGrade: null,
  selectedYear: new Date().getFullYear(),
  isFilterPanelOpen: false,
};

// Reducer function
function studentsAnalysisReducer(state, action) {
  switch (action.type) {
    case 'FETCH_STUDENTS_REQUEST':
      return { ...state, loading: true, error: null };

    case 'FETCH_STUDENTS_SUCCESS':
      return {
        ...state,
        loading: false,
        departmentStats: action.payload.department_stats,
        gradeDistribution: action.payload.grade_distribution,
        enrollmentTrend: action.payload.enrollment_trend,
        error: null,
      };

    case 'FETCH_STUDENTS_FAILURE':
      return { ...state, loading: false, error: action.payload };

    case 'SET_DEPARTMENT_FILTER':
      return { ...state, selectedDepartment: action.payload };

    case 'SET_GRADE_FILTER':
      return { ...state, selectedGrade: action.payload };

    case 'SET_YEAR_FILTER':
      return { ...state, selectedYear: action.payload };

    case 'RESET_FILTERS':
      return {
        ...state,
        selectedDepartment: null,
        selectedGrade: null,
        selectedYear: new Date().getFullYear(),
      };

    case 'TOGGLE_FILTER_PANEL':
      return { ...state, isFilterPanelOpen: !state.isFilterPanelOpen };

    case 'SET_CHART_LOADING':
      return {
        ...state,
        chartLoadingStatus: {
          ...state.chartLoadingStatus,
          [action.payload.chart]: action.payload.loading,
        },
      };

    default:
      return state;
  }
}

const StudentsAnalysisContext = createContext();

export const StudentsAnalysisProvider = ({ children }) => {
  const [state, dispatch] = useReducer(studentsAnalysisReducer, initialState);
  const { getAuthenticatedClient } = useApiClient();

  // Fetch function
  const fetchStudentsData = useCallback(async () => {
    dispatch({ type: 'FETCH_STUDENTS_REQUEST' });

    try {
      const client = await getAuthenticatedClient();
      const params = new URLSearchParams();

      if (state.selectedDepartment) params.append('department', state.selectedDepartment);
      if (state.selectedGrade !== null) params.append('grade', String(state.selectedGrade));
      params.append('year', String(state.selectedYear));

      const response = await client.get(`/students/analytics?${params.toString()}`);

      dispatch({
        type: 'FETCH_STUDENTS_SUCCESS',
        payload: response.data
      });
    } catch (error) {
      dispatch({
        type: 'FETCH_STUDENTS_FAILURE',
        payload: error
      });
    }
  }, [getAuthenticatedClient, state.selectedDepartment, state.selectedGrade, state.selectedYear]);

  // Auto-fetch on filter change
  useEffect(() => {
    fetchStudentsData();
  }, [state.selectedDepartment, state.selectedGrade, state.selectedYear]);

  // Filter handlers
  const setDepartmentFilter = useCallback((department) => {
    dispatch({ type: 'SET_DEPARTMENT_FILTER', payload: department });
  }, []);

  const setGradeFilter = useCallback((grade) => {
    dispatch({ type: 'SET_GRADE_FILTER', payload: grade });
  }, []);

  const setYearFilter = useCallback((year) => {
    dispatch({ type: 'SET_YEAR_FILTER', payload: year });
  }, []);

  const resetFilters = useCallback(() => {
    dispatch({ type: 'RESET_FILTERS' });
  }, []);

  const toggleFilterPanel = useCallback(() => {
    dispatch({ type: 'TOGGLE_FILTER_PANEL' });
  }, []);

  const retryFetch = useCallback(() => {
    return fetchStudentsData();
  }, [fetchStudentsData]);

  // Computed values
  const totalStudents = useMemo(
    () => state.departmentStats.reduce((sum, dept) => sum + dept.student_count, 0),
    [state.departmentStats]
  );

  const departmentCount = useMemo(
    () => state.departmentStats.length,
    [state.departmentStats]
  );

  const averageStudentsPerDepartment = useMemo(
    () => departmentCount > 0 ? totalStudents / departmentCount : 0,
    [totalStudents, departmentCount]
  );

  const largestDepartment = useMemo(() => {
    if (state.departmentStats.length === 0) return null;
    return state.departmentStats.reduce((max, dept) =>
      dept.student_count > max.student_count ? dept : max
    ).department;
  }, [state.departmentStats]);

  // Filter options
  const departmentOptions = useMemo(
    () => [...new Set(state.departmentStats.map(d => d.department))],
    [state.departmentStats]
  );

  const gradeOptions = [1, 2, 3, 4, 0]; // 0 = graduate students
  const yearOptions = [2020, 2021, 2022, 2023, 2024, 2025];

  const value = {
    state,
    fetchStudentsData,
    setDepartmentFilter,
    setGradeFilter,
    setYearFilter,
    resetFilters,
    toggleFilterPanel,
    retryFetch,
    totalStudents,
    departmentCount,
    averageStudentsPerDepartment,
    largestDepartment,
    departmentOptions,
    gradeOptions,
    yearOptions,
  };

  return (
    <StudentsAnalysisContext.Provider value={value}>
      {children}
    </StudentsAnalysisContext.Provider>
  );
};

export const useStudentsAnalysis = () => {
  const context = useContext(StudentsAnalysisContext);
  if (context === undefined) {
    throw new Error('useStudentsAnalysis must be used within StudentsAnalysisProvider');
  }
  return context;
};
