/**
 * Dashboard Page Component
 * Main landing page displaying KPIs, trends, and visualizations.
 * Follows the plan.md specifications.
 */

import { Box, Typography, Alert, Button, Grid } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { MainLayout } from '../layouts/MainLayout';
import { DashboardProvider, useDashboard } from '../context/DashboardContext';
import { KPICardsSection } from '../components/dashboard/KPICardsSection';
import { TrendChartSection } from '../components/dashboard/TrendChartSection';
import { DepartmentChartSection } from '../components/dashboard/DepartmentChartSection';
import { BudgetChartSection } from '../components/dashboard/BudgetChartSection';
import { formatDate } from '../utils/formatters';

/**
 * Dashboard Content Component
 * Displays all dashboard sections and handles errors.
 * Wrapped by DashboardProvider for state management.
 */
const DashboardContent = () => {
  const { error, lastUpdated, clearError, refreshDashboard, isLoading } = useDashboard();

  return (
    <Box sx={{ p: 3 }}>
      {/* Header Section */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            대시보드
          </Typography>
          {lastUpdated && (
            <Typography variant="body2" color="textSecondary">
              마지막 업데이트: {formatDate(lastUpdated)}
            </Typography>
          )}
        </Box>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={refreshDashboard}
          disabled={isLoading}
        >
          새로고침
        </Button>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert
          severity="error"
          action={
            <>
              <Button color="inherit" size="small" onClick={refreshDashboard}>
                재시도
              </Button>
              <Button color="inherit" size="small" onClick={clearError}>
                닫기
              </Button>
            </>
          }
          sx={{ mb: 3 }}
        >
          {error.message}
        </Alert>
      )}

      {/* KPI Cards Section */}
      <Box sx={{ mb: 4 }}>
        <KPICardsSection />
      </Box>

      {/* Charts Section */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TrendChartSection />
        </Grid>
        <Grid item xs={12} md={6}>
          <DepartmentChartSection />
        </Grid>
        <Grid item xs={12} md={6}>
          <BudgetChartSection />
        </Grid>
      </Grid>
    </Box>
  );
};

/**
 * Dashboard Page Component
 * Wraps DashboardContent with DashboardProvider and MainLayout.
 */
const DashboardPage = () => {
  return (
    <MainLayout>
      <DashboardProvider>
        <DashboardContent />
      </DashboardProvider>
    </MainLayout>
  );
};

export default DashboardPage;
