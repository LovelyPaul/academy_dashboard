/**
 * Field Chart Component
 * Bar chart showing publications by field/department
 */
import React, { useMemo } from 'react';
import { Card } from '../../../components/common/Card';
import { BarChart } from '../../../components/charts/BarChart';
import { transformToBarChartData } from '../../../services/dataTransformer';
import { usePapersContext } from '../PapersContext';

export function FieldChart() {
  const { state } = usePapersContext();
  const { fieldData, isLoading } = state;

  const chartData = useMemo(() => {
    if (!fieldData || fieldData.length === 0) {
      return null;
    }
    return transformToBarChartData(fieldData, 'department', 'count', {
      label: 'Publications',
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)'
    });
  }, [fieldData]);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      },
      title: {
        display: true,
        text: 'Publications by Field'
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
      <Card title="Field Statistics">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          Loading...
        </div>
      </Card>
    );
  }

  if (!chartData) {
    return (
      <Card title="Field Statistics">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          No data available
        </div>
      </Card>
    );
  }

  return (
    <Card title="Field Statistics">
      <BarChart data={chartData} options={chartOptions} />
    </Card>
  );
}

export default FieldChart;
