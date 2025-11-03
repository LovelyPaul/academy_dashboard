/**
 * Empty State Component
 *
 * Displays a friendly message when there is no data available.
 * Provides visual feedback and optional action button.
 */
import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import {
  InboxOutlined as InboxIcon,
  BarChartOutlined as ChartIcon,
  UploadFileOutlined as UploadIcon,
  RefreshOutlined as RefreshIcon,
} from '@mui/icons-material';

/**
 * EmptyState Component
 *
 * @param {Object} props
 * @param {string} props.title - Main title text
 * @param {string} props.description - Description text
 * @param {string} props.icon - Icon type ('inbox', 'chart', 'upload', 'refresh')
 * @param {string} props.actionLabel - Optional action button label
 * @param {Function} props.onAction - Optional action button handler
 * @param {boolean} props.minimal - Use minimal styling without Paper wrapper
 */
export function EmptyState({
  title = '데이터가 없습니다',
  description = '아직 표시할 데이터가 없습니다.',
  icon = 'inbox',
  actionLabel,
  onAction,
  minimal = false,
}) {
  // Icon mapping
  const iconMap = {
    inbox: InboxIcon,
    chart: ChartIcon,
    upload: UploadIcon,
    refresh: RefreshIcon,
  };

  const IconComponent = iconMap[icon] || InboxIcon;

  const content = (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        py: 8,
        px: 3,
        textAlign: 'center',
      }}
    >
      {/* Icon */}
      <Box
        sx={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          backgroundColor: 'action.hover',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 3,
        }}
      >
        <IconComponent
          sx={{
            fontSize: 48,
            color: 'action.active',
          }}
        />
      </Box>

      {/* Title */}
      <Typography
        variant="h6"
        component="h3"
        gutterBottom
        sx={{ color: 'text.primary', fontWeight: 500 }}
      >
        {title}
      </Typography>

      {/* Description */}
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ maxWidth: 400, mb: 3 }}
      >
        {description}
      </Typography>

      {/* Action Button */}
      {actionLabel && onAction && (
        <Button variant="contained" color="primary" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </Box>
  );

  // Return with or without Paper wrapper
  if (minimal) {
    return content;
  }

  return (
    <Paper
      elevation={0}
      sx={{
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 2,
      }}
    >
      {content}
    </Paper>
  );
}

export default EmptyState;
