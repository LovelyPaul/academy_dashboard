/**
 * Papers Reducer
 * State management reducer for Papers Analysis page
 * Implements state transitions for data fetching, filtering, and error handling
 */

// Action types
export const FETCH_PAPERS_START = 'FETCH_PAPERS_START';
export const FETCH_PAPERS_SUCCESS = 'FETCH_PAPERS_SUCCESS';
export const FETCH_PAPERS_ERROR = 'FETCH_PAPERS_ERROR';
export const SET_FILTER = 'SET_FILTER';
export const CLEAR_FILTERS = 'CLEAR_FILTERS';
export const RESET_ERROR = 'RESET_ERROR';

// Initial state
export const initialState = {
  papersData: null,
  yearlyData: [],
  journalData: [],
  fieldData: [],
  filters: {
    year: null,
    journal: null,
    field: null
  },
  isLoading: true,
  error: null,
  hasData: false
};

// Reducer function
export function papersReducer(state, action) {
  switch (action.type) {
    case FETCH_PAPERS_START:
      return {
        ...state,
        isLoading: true,
        error: null
      };

    case FETCH_PAPERS_SUCCESS:
      return {
        ...state,
        isLoading: false,
        papersData: action.payload,
        yearlyData: action.payload.yearly_data || [],
        journalData: action.payload.journal_data || [],
        fieldData: action.payload.field_data || [],
        hasData: action.payload.has_data || false,
        error: null
      };

    case FETCH_PAPERS_ERROR:
      return {
        ...state,
        isLoading: false,
        error: action.payload,
        hasData: false
      };

    case SET_FILTER:
      return {
        ...state,
        filters: {
          ...state.filters,
          [action.payload.filterType]: action.payload.value
        }
      };

    case CLEAR_FILTERS:
      return {
        ...state,
        filters: {
          year: null,
          journal: null,
          field: null
        }
      };

    case RESET_ERROR:
      return {
        ...state,
        error: null
      };

    default:
      return state;
  }
}
