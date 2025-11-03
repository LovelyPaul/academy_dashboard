/**
 * Yearly Chart Component
 * Line/Bar chart showing publications by year
 */
import React, { useMemo } from 'react';
import { Card } from '../../../components/common/Card';
import { LineChart } from '../../../components/charts/LineChart';
import { EmptyState } from '../../../components/common/EmptyState';
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
      label: '논문 수',
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
        text: '연도별 논문 수'
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
      <Card title="연도별 논문 수">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          로딩 중...
        </div>
      </Card>
    );
  }

  if (!chartData) {
    return (
      <Card title="연도별 논문 수">
        <EmptyState
          title="논문 데이터가 없습니다"
          description="아직 등록된 논문 데이터가 없습니다. 데이터를 업로드하여 연도별 논문 통계를 확인하세요."
          icon="chart"
          minimal
        />
      </Card>
    );
  }

  return (
    <Card title="연도별 논문 수">
      <LineChart data={chartData} options={chartOptions} />
    </Card>
  );
}

export default YearlyChart;
