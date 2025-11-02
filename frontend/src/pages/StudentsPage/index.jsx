/**
 * StudentsAnalysisPage: Main page component for student analytics
 * Wraps all sections with the StudentsAnalysisProvider for state management
 */
import React from 'react';
import { StudentsAnalysisProvider } from '../../contexts/StudentsAnalysisContext';
import { MainLayout } from '../../layouts/MainLayout';
import { Box, Typography } from '@mui/material';
import { KPISection } from './components/KPISection';
import { FilterSection } from './components/FilterSection';
import { ChartsSection } from './components/ChartsSection';

const StudentsAnalysisPage = () => {
  return (
    <MainLayout>
      <StudentsAnalysisProvider>
        <Box sx={{ p: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            학생 분석
          </Typography>
          <FilterSection />
          <KPISection />
          <ChartsSection />
        </Box>
      </StudentsAnalysisProvider>
    </MainLayout>
  );
};

export default StudentsAnalysisPage;
