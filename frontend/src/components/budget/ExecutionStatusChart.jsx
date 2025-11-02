import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress } from '@mui/material';
import { useBudget } from '../../contexts/BudgetContext';

export default function ExecutionStatusChart() {
  const { state } = useBudget();

  const getProgressColor = (status) => {
    switch (status) {
      case 'critical': return 'error';
      case 'warning': return 'warning';
      default: return 'success';
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>Budget Execution Status</Typography>
        <Box sx={{ maxHeight: '400px', overflowY: 'auto' }}>
          {state.executionStatus.map((item, index) => (
            <Box key={index} sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body1">{item.department}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {item.execution_rate}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={Math.min(item.execution_rate, 100)}
                color={getProgressColor(item.status)}
                sx={{ height: 10, borderRadius: 5 }}
              />
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
}
