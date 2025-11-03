/**
 * Journal Chart Component
 * Pie chart showing journal grade distribution
 */
import React, { useMemo } from 'react';
import { Card } from '../../../components/common/Card';
import { PieChart } from '../../../components/charts/PieChart';
import { EmptyState } from '../../../components/common/EmptyState';
import { transformToPieChartData } from '../../../services/dataTransformer';
import { usePapersContext } from '../PapersContext';

export function JournalChart() {
  const { state } = usePapersContext();
  const { journalData, isLoading } = state;

  const chartData = useMemo(() => {
    if (!journalData || journalData.length === 0) {
      return null;
    }
    return transformToPieChartData(journalData, 'journal_grade', 'count');
  }, [journalData]);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'right'
      },
      title: {
        display: true,
        text: '저널 등급별 논문 분포'
      }
    }
  };

  if (isLoading) {
    return (
      <Card title="저널 등급별 분포">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          로딩 중...
        </div>
      </Card>
    );
  }

  if (!chartData) {
    return (
      <Card title="저널 등급별 분포">
        <EmptyState
          title="저널 등급 데이터가 없습니다"
          description="저널 등급별 논문 분포를 확인할 수 있는 데이터가 없습니다."
          icon="chart"
          minimal
        />
      </Card>
    );
  }

  return (
    <Card title="저널 등급별 분포">
      <PieChart data={chartData} options={chartOptions} />
    </Card>
  );
}

export default JournalChart;
