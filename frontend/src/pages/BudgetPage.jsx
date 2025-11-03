import React from 'react';
import { BudgetProvider, useBudget } from '../contexts/BudgetContext';
import MainLayout from '../layouts/MainLayout';
import { Box, Typography, Alert, Button, CircularProgress } from '@mui/material';
import BudgetFilters from '../components/budget/BudgetFilters';
import BudgetKPISection from '../components/budget/BudgetKPISection';
import BudgetAllocationChart from '../components/budget/BudgetAllocationChart';
import ExecutionStatusChart from '../components/budget/ExecutionStatusChart';
import YearlyTrendsChart from '../components/budget/YearlyTrendsChart';
import BudgetDataTable from '../components/budget/BudgetDataTable';

function BudgetPageContent() {
  const {
    state,
    overallExecutionRate,
    totalBudget,
    totalExecuted,
    totalRemaining,
    warningDepartments,
    criticalDepartments,
    isLoading,
    updateFilter,
    resetFilters,
    toggleView,
    retryFetch,
  } = useBudget();

  // Loading state
  if (isLoading) {
    return (
      <MainLayout>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
          <CircularProgress size={60} />
        </Box>
      </MainLayout>
    );
  }

  // Error state
  if (state.error) {
    return (
      <MainLayout>
        <Alert
          severity="error"
          action={
            <Button color="inherit" size="small" onClick={retryFetch}>
              다시 시도
            </Button>
          }
        >
          {state.error.message}
        </Alert>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <Box sx={{ p: 3 }}>
        {/* Page Header */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            예산 분석
          </Typography>
          <Typography variant="body2" color="textSecondary">
            부서별 예산 배정, 집행 현황 및 연도별 추이
          </Typography>
        </Box>

        {/* Filters */}
        <BudgetFilters
          filters={state.filters}
          onFilterChange={updateFilter}
          onReset={resetFilters}
        />

        {/* KPI Summary */}
        <BudgetKPISection
          totalBudget={totalBudget}
          totalExecuted={totalExecuted}
          totalRemaining={totalRemaining}
          executionRate={overallExecutionRate}
          warningCount={warningDepartments}
          criticalCount={criticalDepartments}
        />

        {/* View Toggle */}
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant={state.selectedView === 'chart' ? 'contained' : 'outlined'}
            onClick={() => toggleView('chart')}
            sx={{ mr: 1 }}
          >
            차트 보기
          </Button>
          <Button
            variant={state.selectedView === 'table' ? 'contained' : 'outlined'}
            onClick={() => toggleView('table')}
          >
            표 보기
          </Button>
        </Box>

        {/* Chart or Table View */}
        {state.selectedView === 'chart' ? (
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
            <BudgetAllocationChart />
            <ExecutionStatusChart />
            <Box sx={{ gridColumn: { xs: 'auto', md: '1 / -1' } }}>
              <YearlyTrendsChart />
            </Box>
          </Box>
        ) : (
          <BudgetDataTable />
        )}
      </Box>
    </MainLayout>
  );
}

export default function BudgetPage() {
  return (
    <BudgetProvider>
      <BudgetPageContent />
    </BudgetProvider>
  );
}
