import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { Pie } from 'react-chartjs-2';
import { useBudget } from '../../contexts/BudgetContext';

export default function BudgetAllocationChart() {
  const { state } = useBudget();

  const chartData = {
    labels: state.budgetAllocation.map(item => item.department),
    datasets: [{
      data: state.budgetAllocation.map(item => item.total_budget),
      backgroundColor: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#FF6384', '#C9CBCF'
      ],
    }]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'right' },
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>Department Budget Allocation</Typography>
        <div style={{ height: '400px' }}>
          <Pie data={chartData} options={options} />
        </div>
      </CardContent>
    </Card>
  );
}
