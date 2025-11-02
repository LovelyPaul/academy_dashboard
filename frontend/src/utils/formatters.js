/**
 * Data formatting utility functions.
 * Following the common-modules.md specification.
 */

/**
 * Format number with thousand separators.
 *
 * @param {number} num - Number to format
 * @returns {string} Formatted number (e.g., "1,000,000")
 */
export const formatNumber = (num) => {
  if (num === null || num === undefined) return '-';
  return num.toLocaleString('ko-KR');
};

/**
 * Format amount to Korean currency format.
 *
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency (e.g., "1,000,000원")
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '-';
  return `${formatNumber(amount)}원`;
};

/**
 * Format value to percentage format.
 *
 * @param {number} value - Percentage value
 * @param {number} decimals - Number of decimal places (default: 1)
 * @returns {string} Formatted percentage (e.g., "85.5%")
 */
export const formatPercentage = (value, decimals = 1) => {
  if (value === null || value === undefined) return '-';
  return `${value.toFixed(decimals)}%`;
};

/**
 * Format date to Korean format.
 *
 * @param {string|Date} dateString - Date string or Date object
 * @returns {string} Formatted date (e.g., "2024년 1월 1일")
 */
export const formatDate = (dateString) => {
  if (!dateString) return '-';

  const date = typeof dateString === 'string' ? new Date(dateString) : dateString;

  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Format date to short format.
 *
 * @param {string|Date} dateString - Date string or Date object
 * @returns {string} Formatted date (e.g., "2024-01-01")
 */
export const formatDateShort = (dateString) => {
  if (!dateString) return '-';

  const date = typeof dateString === 'string' ? new Date(dateString) : dateString;

  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).replace(/\. /g, '-').replace('.', '');
};

/**
 * Truncate text with ellipsis.
 *
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 50) => {
  if (!text) return '-';
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

export default {
  formatNumber,
  formatCurrency,
  formatPercentage,
  formatDate,
  formatDateShort,
  truncateText,
};
