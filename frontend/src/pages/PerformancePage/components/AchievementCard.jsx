import React from 'react';
import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Typography,
  LinearProgress,
  Chip
} from '@mui/material';
import { EmojiEvents } from '@mui/icons-material';
import { formatPercentage } from '../../../utils/formatters';
import { usePerformanceContext } from '../PerformanceContext';

/**
 * Achievement Card Component
 *
 * Displays target achievement rate with visual indicators
 */
export default function AchievementCard() {
  const { state } = usePerformanceContext();
  const { performanceData } = state;

  if (!performanceData?.achievementData) {
    return null;
  }

  const { actual, target, rate, status } = performanceData.achievementData;

  // Color based on status (BR-3)
  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return 'success';
      case 'warning':
        return 'warning';
      case 'danger':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusLabel = () => {
    switch (status) {
      case 'success':
        return '목표 달성';
      case 'warning':
        return '주의';
      case 'danger':
        return '미달성';
      default:
        return '목표 미설정';
    }
  };

  const getStatusTextColor = () => {
    switch (status) {
      case 'success':
        return 'success.main';
      case 'warning':
        return 'warning.main';
      case 'danger':
        return 'error.main';
      default:
        return 'text.secondary';
    }
  };

  return (
    <Card>
      <CardHeader
        title="목표 대비 달성률"
        avatar={<EmojiEvents />}
        action={
          <Chip
            label={getStatusLabel()}
            color={getStatusColor()}
            size="small"
          />
        }
      />
      <CardContent>
        {/* Achievement Rate */}
        <Box textAlign="center" mb={3}>
          <Typography variant="h2" component="div" color={getStatusTextColor()}>
            {rate !== null ? formatPercentage(rate) : 'N/A'}
          </Typography>
        </Box>

        {/* Progress Bar */}
        {rate !== null && (
          <Box mb={3}>
            <LinearProgress
              variant="determinate"
              value={Math.min(rate, 100)}
              color={getStatusColor()}
              sx={{ height: 10, borderRadius: 5 }}
            />
          </Box>
        )}

        {/* Actual vs Target */}
        <Box>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <Typography variant="body2" color="textSecondary">
              실제 실적
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {actual.toFixed(2)}%
            </Typography>
          </Box>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="body2" color="textSecondary">
              목표 실적
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {target.toFixed(2)}%
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
