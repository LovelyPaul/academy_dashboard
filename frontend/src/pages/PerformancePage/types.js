import PropTypes from 'prop-types';

/**
 * Trend data point type
 */
export const TrendDataPointType = PropTypes.shape({
  date: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  target: PropTypes.number,
});

/**
 * Department data point type
 */
export const DepartmentDataPointType = PropTypes.shape({
  department: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  percentage: PropTypes.number,
});

/**
 * Achievement data type
 */
export const AchievementDataType = PropTypes.shape({
  actual: PropTypes.number.isRequired,
  target: PropTypes.number.isRequired,
  rate: PropTypes.number,
  status: PropTypes.oneOf(['success', 'warning', 'danger', 'unknown']).isRequired,
});

/**
 * Performance data type (complete)
 */
export const PerformanceDataType = PropTypes.shape({
  trendData: PropTypes.arrayOf(TrendDataPointType).isRequired,
  departmentData: PropTypes.arrayOf(DepartmentDataPointType).isRequired,
  achievementData: AchievementDataType.isRequired,
});

/**
 * Filter state type
 */
export const FilterStateType = PropTypes.shape({
  startDate: PropTypes.string.isRequired,
  endDate: PropTypes.string.isRequired,
  department: PropTypes.string,
  project: PropTypes.string,
});

/**
 * Loading state type
 */
export const LoadingStateType = PropTypes.shape({
  initial: PropTypes.bool.isRequired,
  filter: PropTypes.bool.isRequired,
});

/**
 * Error state type
 */
export const ErrorStateType = PropTypes.shape({
  type: PropTypes.oneOf(['network', 'auth', 'validation', 'data']).isRequired,
  message: PropTypes.string.isRequired,
});
