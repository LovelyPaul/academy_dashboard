import React, { useMemo } from 'react';
import { Card, CardHeader, CardContent, Box, Typography, CircularProgress } from '@mui/material';
import { TrendingUp } from '@mui/icons-material';
import { LineChart } from '../../../components/charts/LineChart';
import { usePerformanceContext } from '../PerformanceContext';

/**
 * Trend Chart Component
 *
 * Displays performance trend over time using line chart
 */
export default function TrendChart() {
  const { state } = usePerformanceContext();
  const { performanceData, loadingState } = state;

  // Transform data for LineChart component
  const chartData = useMemo(() => {
    if (!performanceData?.trendData || performanceData.trendData.length === 0) {
      return null;
    }

    const labels = performanceData.trendData.map(item => item.date);
    const values = performanceData.trendData.map(item => item.value);
    const targets = performanceData.trendData.map(item => item.target || null);

    return {
      labels,
      datasets: [
        {
          label: '실적',
          data: values,
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1,
        },
        {
          label: '목표',
          data: targets,
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderDash: [5, 5],
          tension: 0.1,
        },
      ],
    };
  }, [performanceData?.trendData]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`;
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
          title="기간별 실적 추이"
          avatar={<TrendingUp />}
        />
        <CardContent>
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight={300}
          >
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
          title="기간별 실적 추이"
          avatar={<TrendingUp />}
        />
        <CardContent>
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight={300}
          >
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
        title="기간별 실적 추이"
        avatar={<TrendingUp />}
        subheader="연도별 실적 변화를 확인하세요"
      />
      <CardContent>
        <Box height={300}>
          <LineChart data={chartData} options={chartOptions} />
        </Box>
      </CardContent>
    </Card>
  );
}
