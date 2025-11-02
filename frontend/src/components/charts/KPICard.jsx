/**
 * KPI Card component for displaying key performance indicators.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

/**
 * KPI Card component for dashboard metrics.
 * Displays a title, main value, and optional subtitle.
 *
 * @param {Object} props - Component props
 * @param {string} props.title - KPI title
 * @param {string|number} props.value - Main KPI value
 * @param {string} props.subtitle - Optional subtitle/description
 * @param {string} props.color - Card accent color (default: 'primary')
 * @returns {JSX.Element} KPI Card component
 */
export const KPICard = ({ title, value, subtitle, color = 'primary' }) => {
  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        borderTop: 3,
        borderColor: `${color}.main`,
      }}
    >
      <CardContent>
        <Typography variant="h6" color="textSecondary" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h3" component="div" color={`${color}.main`}>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default KPICard;
