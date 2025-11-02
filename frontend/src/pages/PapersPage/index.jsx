/**
 * Papers Analysis Page
 *
 * Main page component for papers analytics dashboard.
 * Displays yearly trends, journal distribution, and field statistics
 * with filtering capabilities.
 *
 * Route: /dashboard/papers
 */
import React from 'react';
import { Box, Typography, Grid } from '@mui/material';
import { MainLayout } from '../../layouts/MainLayout';
import { PapersProvider } from './PapersContext';
import { FilterSection } from './components/FilterSection';
import { YearlyChart } from './components/YearlyChart';
import { JournalChart } from './components/JournalChart';
import { FieldChart } from './components/FieldChart';
import { LoadingOverlay } from './components/LoadingOverlay';
import { ErrorBanner } from './components/ErrorBanner';

/**
 * Papers Page Content Component
 *
 * Inner component that consumes the Papers context.
 * Renders all page elements including filters and charts.
 */
function PapersPageContent() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Papers Analysis
      </Typography>

      <ErrorBanner />

      <FilterSection />

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <YearlyChart />
        </Grid>

        <Grid item xs={12} md={6}>
          <JournalChart />
        </Grid>

        <Grid item xs={12} md={6}>
          <FieldChart />
        </Grid>
      </Grid>

      <LoadingOverlay />
    </Box>
  );
}

/**
 * Papers Page Component
 *
 * Main export that wraps content with providers.
 * Provides layout and context to all child components.
 */
export function PapersPage() {
  return (
    <MainLayout>
      <PapersProvider>
        <PapersPageContent />
      </PapersProvider>
    </MainLayout>
  );
}

export default PapersPage;
