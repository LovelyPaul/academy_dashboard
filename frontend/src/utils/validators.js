/**
 * Client-side validation utility functions.
 * Following the common-modules.md specification.
 */

/**
 * Validate email format.
 *
 * @param {string} email - Email string to validate
 * @returns {boolean} True if valid email format
 */
export const isValidEmail = (email) => {
  if (!email) return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate file extension.
 *
 * @param {File} file - File object to validate
 * @param {Array<string>} allowedExtensions - Array of allowed extensions (e.g., ['xlsx', 'xls'])
 * @returns {boolean} True if file extension is allowed
 */
export const isValidFileExtension = (file, allowedExtensions) => {
  if (!file || !file.name) return false;

  const extension = file.name.split('.').pop().toLowerCase();
  return allowedExtensions.map(ext => ext.toLowerCase()).includes(extension);
};

/**
 * Validate file size.
 *
 * @param {File} file - File object to validate
 * @param {number} maxSizeMB - Maximum size in MB
 * @returns {boolean} True if file size is within limit
 */
export const isValidFileSize = (file, maxSizeMB) => {
  if (!file) return false;

  const maxSizeBytes = maxSizeMB * 1024 * 1024;
  return file.size <= maxSizeBytes;
};

/**
 * Validate required field.
 *
 * @param {any} value - Value to validate
 * @returns {boolean} True if value is not empty
 */
export const isRequired = (value) => {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  return true;
};

/**
 * Validate number range.
 *
 * @param {number} value - Number to validate
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {boolean} True if number is within range
 */
export const isInRange = (value, min, max) => {
  const num = Number(value);
  if (isNaN(num)) return false;
  return num >= min && num <= max;
};

/**
 * Validate year.
 *
 * @param {number} year - Year to validate
 * @returns {boolean} True if year is valid (2000-2100)
 */
export const isValidYear = (year) => {
  return isInRange(year, 2000, 2100);
};

export default {
  isValidEmail,
  isValidFileExtension,
  isValidFileSize,
  isRequired,
  isInRange,
  isValidYear,
};
