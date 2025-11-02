import React, { useMemo } from 'react';
import { Card, CardHeader, CardContent, Box, Typography, CircularProgress } from '@mui/material';
import { BarChart as BarChartIcon } from '@mui/icons-material';
import { BarChart } from '../../../components/charts/BarChart';
import { usePerformanceContext } from '../PerformanceContext';

/**
 * Department Chart Component
 *
 * Displays department performance comparison using bar chart
 */
export default function DepartmentChart() {
  const { state } = usePerformanceContext();
  const { performanceData, loadingState } = state;

  // Transform data for BarChart component
  const chartData = useMemo(() => {
    if (!performanceData?.departmentData || performanceData.departmentData.length === 0) {
      return null;
    }

    const labels = performanceData.departmentData.map(item => item.department);
    const values = performanceData.departmentData.map(item => item.value);

    return {
      labels,
      datasets: [
        {
          label: '부서별 실적',
          data: values,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    };
  }, [performanceData?.departmentData]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const dataPoint = performanceData.departmentData[context.dataIndex];
            const percentage = dataPoint.percentage
              ? ` (${dataPoint.percentage.toFixed(1)}%)`
              : '';
            return `실적: ${context.parsed.y.toFixed(2)}%${percentage}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => `${value}%`
        }
      }
    }
  };

  // Loading overlay
  if (loadingState.filter) {
    return (
      <Card>
        <CardHeader
          title="부서별 실적 비교"
          avatar={<BarChartIcon />}
        />
        <CardContent>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={300}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  // Empty state
  if (!chartData) {
    return (
      <Card>
        <CardHeader
          title="부서별 실적 비교"
          avatar={<BarChartIcon />}
        />
        <CardContent>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={300}>
            <Typography color="textSecondary">
              표시할 데이터가 없습니다
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader
        title="부서별 실적 비교"
        avatar={<BarChartIcon />}
        subheader="부서별 실적을 비교하세요"
      />
      <CardContent>
        <Box height={300}>
          <BarChart data={chartData} options={chartOptions} />
        </Box>
      </CardContent>
    </Card>
  );
}
