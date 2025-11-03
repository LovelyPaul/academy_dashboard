/**
 * Field Chart Component
 * Bar chart showing publications by field/department
 */
import React, { useMemo } from 'react';
import { Card } from '../../../components/common/Card';
import { BarChart } from '../../../components/charts/BarChart';
import { EmptyState } from '../../../components/common/EmptyState';
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
      label: '논문 수',
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
        text: '분야별 논문 수'
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
      <Card title="분야별 통계">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          로딩 중...
        </div>
      </Card>
    );
  }

  if (!chartData) {
    return (
      <Card title="분야별 통계">
        <EmptyState
          title="분야별 데이터가 없습니다"
          description="분야별 논문 통계를 확인할 수 있는 데이터가 없습니다."
          icon="chart"
          minimal
        />
      </Card>
    );
  }

  return (
    <Card title="분야별 통계">
      <BarChart data={chartData} options={chartOptions} />
    </Card>
  );
}

export default FieldChart;
