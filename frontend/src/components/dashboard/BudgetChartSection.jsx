/**
 * Budget Chart Section Component
 * Displays pie chart for budget allocation.
 * Follows the plan.md specifications.
 */

import { Card, CardHeader, CardContent, Skeleton } from '@mui/material';
import { useDashboard } from '../../context/DashboardContext';
import { PieChart } from '../charts/PieChart';
import { transformToPieChartData } from '../../services/dataTransformer';

/**
 * Budget Chart Section Component
 * Renders a pie chart showing budget allocation by department.
 */
export const BudgetChartSection = () => {
  const { budgetData, isLoading } = useDashboard();

  // Show loading skeleton
  if (isLoading) {
    return (
      <Card>
        <CardHeader title="예산 배분 현황" />
        <CardContent>
          <Skeleton variant="circular" width={300} height={300} sx={{ margin: '0 auto' }} />
        </CardContent>
      </Card>
    );
  }

  // Show empty state if no data
  if (!budgetData || budgetData.length === 0) {
    return (
      <Card>
        <CardHeader title="예산 배분 현황" />
        <CardContent>
          <p>데이터가 없습니다.</p>
        </CardContent>
      </Card>
    );
  }

  // Transform data for chart
  const chartData = transformToPieChartData(budgetData, 'category', 'value');

  // Chart options
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'right',
      },
    },
  };

  return (
    <Card>
      <CardHeader title="예산 배분 현황" />
      <CardContent sx={{ height: 300 }}>
        <PieChart data={chartData} options={options} />
      </CardContent>
    </Card>
  );
};
