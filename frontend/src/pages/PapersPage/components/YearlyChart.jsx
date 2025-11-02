/**
 * Yearly Chart Component
 * Line/Bar chart showing publications by year
 */
import React, { useMemo } from 'react';
import { Card } from '../../../components/common/Card';
import { LineChart } from '../../../components/charts/LineChart';
import { transformToLineChartData } from '../../../services/dataTransformer';
import { usePapersContext } from '../PapersContext';

export function YearlyChart() {
  const { state } = usePapersContext();
  const { yearlyData, isLoading } = state;

  const chartData = useMemo(() => {
    if (!yearlyData || yearlyData.length === 0) {
      return null;
    }
    return transformToLineChartData(yearlyData, 'year', 'count', {
      label: 'Publications',
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)'
    });
  }, [yearlyData]);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      },
      title: {
        display: true,
        text: 'Publications by Year'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 10
        }
      }
    }
  };

  if (isLoading) {
    return (
      <Card title="Publications by Year">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          Loading...
        </div>
      </Card>
    );
  }

  if (!chartData) {
    return (
      <Card title="Publications by Year">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          No data available
        </div>
      </Card>
    );
  }

  return (
    <Card title="Publications by Year">
      <LineChart data={chartData} options={chartOptions} />
    </Card>
  );
}

export default YearlyChart;
