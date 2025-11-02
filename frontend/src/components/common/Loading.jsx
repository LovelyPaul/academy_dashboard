/**
 * Reusable Loading indicator component.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { CircularProgress, Box } from '@mui/material';

/**
 * Custom Loading component displaying a centered spinner.
 * Used for async data loading states.
 *
 * @param {Object} props - Component props
 * @param {number} props.size - Size of the spinner (default: 40)
 * @param {string} props.color - Color of the spinner (default: 'primary')
 * @returns {JSX.Element} Loading component
 */
export const Loading = ({ size = 40, color = 'primary' }) => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="200px"
    >
      <CircularProgress size={size} color={color} />
    </Box>
  );
};

export default Loading;
