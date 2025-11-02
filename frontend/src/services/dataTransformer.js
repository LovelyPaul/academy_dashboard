/**
 * Data transformation utilities for chart libraries.
 * Following the common-modules.md specification.
 * Converts API response data to Chart.js format.
 */

/**
 * Transform data to Bar Chart format.
 *
 * @param {Array} data - API response data array
 * @param {string} labelKey - Key for chart labels
 * @param {string} valueKey - Key for chart values
 * @param {Object} options - Additional options
 * @returns {Object} Chart.js compatible data object
 */
export const transformToBarChartData = (data, labelKey, valueKey, options = {}) => {
  const {
    backgroundColor = 'rgba(75, 192, 192, 0.6)',
    borderColor = 'rgba(75, 192, 192, 1)',
    label = valueKey,
  } = options;

  return {
    labels: data.map((item) => item[labelKey]),
    datasets: [
      {
        label,
        data: data.map((item) => item[valueKey]),
        backgroundColor,
        borderColor,
        borderWidth: 1,
      },
    ],
  };
};

/**
 * Transform data to Line Chart format.
 *
 * @param {Array} data - API response data array
 * @param {string} labelKey - Key for chart labels
 * @param {string} valueKey - Key for chart values
 * @param {Object} options - Additional options
 * @returns {Object} Chart.js compatible data object
 */
export const transformToLineChartData = (data, labelKey, valueKey, options = {}) => {
  const {
    borderColor = 'rgb(75, 192, 192)',
    backgroundColor = 'rgba(75, 192, 192, 0.2)',
    label = valueKey,
    tension = 0.1,
  } = options;

  return {
    labels: data.map((item) => item[labelKey]),
    datasets: [
      {
        label,
        data: data.map((item) => item[valueKey]),
        borderColor,
        backgroundColor,
        tension,
        fill: true,
      },
    ],
  };
};

/**
 * Transform data to Pie Chart format.
 *
 * @param {Array} data - API response data array
 * @param {string} labelKey - Key for chart labels
 * @param {string} valueKey - Key for chart values
 * @param {Object} options - Additional options
 * @returns {Object} Chart.js compatible data object
 */
export const transformToPieChartData = (data, labelKey, valueKey, options = {}) => {
  const {
    backgroundColor = [
      'rgba(255, 99, 132, 0.6)',
      'rgba(54, 162, 235, 0.6)',
      'rgba(255, 206, 86, 0.6)',
      'rgba(75, 192, 192, 0.6)',
      'rgba(153, 102, 255, 0.6)',
      'rgba(255, 159, 64, 0.6)',
    ],
  } = options;

  return {
    labels: data.map((item) => item[labelKey]),
    datasets: [
      {
        data: data.map((item) => item[valueKey]),
        backgroundColor,
        borderColor: backgroundColor.map(color => color.replace('0.6', '1')),
        borderWidth: 1,
      },
    ],
  };
};

/**
 * Transform data for multiple datasets (e.g., comparing multiple metrics).
 *
 * @param {Array} data - API response data array
 * @param {string} labelKey - Key for chart labels
 * @param {Array} valueKeys - Array of value keys for multiple datasets
 * @param {string} chartType - Type of chart ('bar' or 'line')
 * @returns {Object} Chart.js compatible data object
 */
export const transformToMultiDatasetChart = (data, labelKey, valueKeys, chartType = 'bar') => {
  const colors = [
    'rgba(75, 192, 192, 0.6)',
    'rgba(255, 99, 132, 0.6)',
    'rgba(255, 206, 86, 0.6)',
    'rgba(153, 102, 255, 0.6)',
    'rgba(54, 162, 235, 0.6)',
  ];

  const datasets = valueKeys.map((key, index) => ({
    label: key,
    data: data.map((item) => item[key]),
    backgroundColor: colors[index % colors.length],
    borderColor: colors[index % colors.length].replace('0.6', '1'),
    borderWidth: chartType === 'bar' ? 1 : 2,
    tension: chartType === 'line' ? 0.1 : undefined,
  }));

  return {
    labels: data.map((item) => item[labelKey]),
    datasets,
  };
};

export default {
  transformToBarChartData,
  transformToLineChartData,
  transformToPieChartData,
  transformToMultiDatasetChart,
};
