/**
 * Trend Chart Section Component
 * Displays line chart for yearly trends.
 * Follows the plan.md specifications.
 */

import { Card, CardHeader, CardContent, Skeleton } from '@mui/material';
import { useDashboard } from '../../context/DashboardContext';
import { LineChart } from '../charts/LineChart';
import { transformToLineChartData } from '../../services/dataTransformer';

/**
 * Trend Chart Section Component
 * Renders a line chart showing yearly performance trends.
 */
export const TrendChartSection = () => {
  const { trendData, isLoading } = useDashboard();

  // Show loading skeleton
  if (isLoading) {
    return (
      <Card>
        <CardHeader title="기간별 추이" />
        <CardContent>
          <Skeleton variant="rectangular" height={300} />
        </CardContent>
      </Card>
    );
  }

  // Show empty state if no data
  if (!trendData || trendData.length === 0) {
    return (
      <Card>
        <CardHeader title="기간별 추이" />
        <CardContent>
          <p>데이터가 없습니다.</p>
        </CardContent>
      </Card>
    );
  }

  // Transform data for chart
  const chartData = transformToLineChartData(trendData, 'year', 'value');

  // Chart options
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  return (
    <Card>
      <CardHeader title="기간별 추이" />
      <CardContent sx={{ height: 300 }}>
        <LineChart data={chartData} options={options} />
      </CardContent>
    </Card>
  );
};
