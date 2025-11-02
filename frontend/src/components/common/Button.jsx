/**
 * Reusable Button component.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Button as MuiButton } from '@mui/material';

/**
 * Custom Button component wrapping MUI Button.
 * Provides consistent styling and props across the application.
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Button content
 * @param {string} props.variant - Button variant (contained, outlined, text)
 * @param {string} props.color - Button color (primary, secondary, error, etc.)
 * @param {boolean} props.fullWidth - Whether button should take full width
 * @param {boolean} props.disabled - Whether button is disabled
 * @param {Function} props.onClick - Click handler
 * @returns {JSX.Element} Button component
 */
export const Button = ({
  children,
  variant = 'contained',
  color = 'primary',
  fullWidth = false,
  disabled = false,
  onClick,
  ...rest
}) => {
  return (
    <MuiButton
      variant={variant}
      color={color}
      fullWidth={fullWidth}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      {children}
    </MuiButton>
  );
};

export default Button;
