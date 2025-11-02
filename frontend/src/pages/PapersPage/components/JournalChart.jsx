/**
 * Journal Chart Component
 * Pie chart showing journal grade distribution
 */
import React, { useMemo } from 'react';
import { Card } from '../../../components/common/Card';
import { PieChart } from '../../../components/charts/PieChart';
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
        text: 'Publications by Journal Grade'
      }
    }
  };

  if (isLoading) {
    return (
      <Card title="Journal Grade Distribution">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          Loading...
        </div>
      </Card>
    );
  }

  if (!chartData) {
    return (
      <Card title="Journal Grade Distribution">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          No data available
        </div>
      </Card>
    );
  }

  return (
    <Card title="Journal Grade Distribution">
      <PieChart data={chartData} options={chartOptions} />
    </Card>
  );
}

export default JournalChart;
