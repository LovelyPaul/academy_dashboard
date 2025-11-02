/**
 * Reusable Card component.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Card as MuiCard, CardContent, CardHeader } from '@mui/material';

/**
 * Custom Card component wrapping MUI Card.
 * Provides consistent styling for card-based layouts.
 *
 * @param {Object} props - Component props
 * @param {string} props.title - Card title (optional)
 * @param {React.ReactNode} props.children - Card content
 * @param {Object} props.sx - Additional sx styles
 * @returns {JSX.Element} Card component
 */
export const Card = ({ title, children, sx = {}, ...rest }) => {
  return (
    <MuiCard sx={{ ...sx }} {...rest}>
      {title && <CardHeader title={title} />}
      <CardContent>{children}</CardContent>
    </MuiCard>
  );
};

export default Card;
