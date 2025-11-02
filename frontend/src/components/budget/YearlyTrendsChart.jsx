import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { useBudget } from '../../contexts/BudgetContext';

export default function YearlyTrendsChart() {
  const { state } = useBudget();

  const chartData = {
    labels: state.yearlyTrends.map(item => item.year.toString()),
    datasets: [
      {
        label: 'Total Budget',
        data: state.yearlyTrends.map(item => item.total_budget),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1
      },
      {
        label: 'Executed Amount',
        data: state.yearlyTrends.map(item => item.executed_amount),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.1
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
    },
    scales: {
      y: { beginAtZero: true }
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>Year-over-Year Budget Trends</Typography>
        <div style={{ height: '400px' }}>
          <Line data={chartData} options={options} />
        </div>
      </CardContent>
    </Card>
  );
}
