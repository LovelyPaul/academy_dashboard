import React from 'react';
import { Box, Grid, Card, CardContent, Typography } from '@mui/material';
import { formatCurrency, formatPercentage } from '../../utils/formatters';

export default function BudgetKPISection({
  totalBudget,
  totalExecuted,
  totalRemaining,
  executionRate,
  warningCount,
  criticalCount
}) {
  const kpiData = [
    { title: 'Total Budget', value: formatCurrency(totalBudget), color: 'primary.main' },
    { title: 'Total Executed', value: formatCurrency(totalExecuted), color: 'success.main' },
    { title: 'Remaining', value: formatCurrency(totalRemaining), color: 'info.main' },
    { title: 'Execution Rate', value: formatPercentage(executionRate), color: executionRate >= 90 ? 'error.main' : 'success.main' },
    { title: 'Warning Departments', value: warningCount, color: 'warning.main' },
    { title: 'Critical Departments', value: criticalCount, color: 'error.main' },
  ];

  return (
    <Box sx={{ mb: 3 }}>
      <Grid container spacing={2}>
        {kpiData.map((kpi, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="textSecondary">{kpi.title}</Typography>
                <Typography variant="h5" sx={{ color: kpi.color }}>{kpi.value}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
