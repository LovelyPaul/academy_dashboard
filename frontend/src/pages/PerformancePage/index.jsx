import React from 'react';
import { Box, Container, Typography, Grid } from '@mui/material';
import { MainLayout } from '../../layouts/MainLayout';
import { PerformanceProvider, usePerformanceContext } from './PerformanceContext';
import FilterPanel from './components/FilterPanel';
import TrendChart from './components/TrendChart';
import DepartmentChart from './components/DepartmentChart';
import AchievementCard from './components/AchievementCard';
import ErrorMessage from './components/ErrorMessage';
import SkeletonLoader from './components/SkeletonLoader';

/**
 * Performance Analysis Page Content
 *
 * Route: /dashboard/performance
 * Use Case: UC-005
 */
function PerformancePageContent() {
  const { state } = usePerformanceContext();
  const { loadingState, error } = state;

  // Initial loading state
  if (loadingState.initial) {
    return <SkeletonLoader />;
  }

  // Error state
  if (error) {
    return (
      <Box>
        <Box mb={3}>
          <Typography variant="h4" component="h1" gutterBottom>
            실적 분석
          </Typography>
          <Typography variant="body2" color="textSecondary">
            부서별 및 기간별 실적 데이터를 분석합니다
          </Typography>
        </Box>
        <ErrorMessage />
      </Box>
    );
  }

  // Success state - render all components
  return (
    <Box>
      {/* Page Header */}
      <Box mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          실적 분석
        </Typography>
        <Typography variant="body2" color="textSecondary">
          부서별 및 기간별 실적 데이터를 분석합니다
        </Typography>
      </Box>

      {/* Filter Panel */}
      <FilterPanel />

      {/* Charts Grid */}
      <Grid container spacing={3}>
        {/* Trend Chart - Full Width */}
        <Grid item xs={12}>
          <TrendChart />
        </Grid>

        {/* Department Chart - 8 columns */}
        <Grid item xs={12} md={8}>
          <DepartmentChart />
        </Grid>

        {/* Achievement Card - 4 columns */}
        <Grid item xs={12} md={4}>
          <AchievementCard />
        </Grid>
      </Grid>
    </Box>
  );
}

/**
 * Performance Analysis Page
 *
 * Main page component with context provider
 */
export default function PerformancePage() {
  return (
    <MainLayout>
      <Container maxWidth="lg">
        <PerformanceProvider>
          <PerformancePageContent />
        </PerformanceProvider>
      </Container>
    </MainLayout>
  );
}
