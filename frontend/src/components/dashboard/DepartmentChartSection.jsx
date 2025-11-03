/**
 * Department Chart Section Component
 * Displays bar chart for department performance comparison.
 * Follows the plan.md specifications.
 */

import { Card, CardHeader, CardContent, Skeleton } from '@mui/material';
import { useDashboard } from '../../context/DashboardContext';
import { BarChart } from '../charts/BarChart';
import { EmptyState } from '../common/EmptyState';
import { transformToBarChartData } from '../../services/dataTransformer';

/**
 * Department Chart Section Component
 * Renders a bar chart showing department performance comparison.
 */
export const DepartmentChartSection = () => {
  const { departmentData, isLoading } = useDashboard();

  // Show loading skeleton
  if (isLoading) {
    return (
      <Card>
        <CardHeader title="부서별 성과 비교" />
        <CardContent>
          <Skeleton variant="rectangular" height={300} />
        </CardContent>
      </Card>
    );
  }

  // Show empty state if no data
  if (!departmentData || departmentData.length === 0) {
    return (
      <Card>
        <CardHeader title="부서별 성과 비교" />
        <CardContent>
          <EmptyState
            title="부서 데이터가 없습니다"
            description="부서별 성과를 비교할 수 있는 데이터가 없습니다."
            icon="chart"
            minimal
          />
        </CardContent>
      </Card>
    );
  }

  // Transform data for chart
  const chartData = transformToBarChartData(departmentData, 'department', 'value');

  // Chart options
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <Card>
      <CardHeader title="부서별 성과 비교" />
      <CardContent sx={{ height: 300 }}>
        <BarChart data={chartData} options={options} />
      </CardContent>
    </Card>
  );
};
