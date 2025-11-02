/**
 * KPISection: Display KPI cards with key student metrics
 * Uses computed values from StudentsAnalysisContext
 */
import React from 'react';
import { Grid, Box, CircularProgress } from '@mui/material';
import { useStudentsAnalysis } from '../../../contexts/StudentsAnalysisContext';
import { KPICard } from '../../../components/charts/KPICard';
import { formatNumber } from '../../../utils/formatters';

export const KPISection = () => {
  const {
    totalStudents,
    departmentCount,
    averageStudentsPerDepartment,
    largestDepartment,
    state
  } = useStudentsAnalysis();

  if (state.loading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ my: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="총 학생 수"
            value={formatNumber(totalStudents)}
            subtitle="재학생"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="학과 수"
            value={formatNumber(departmentCount)}
            subtitle="전체 학과"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="학과당 평균"
            value={formatNumber(Math.round(averageStudentsPerDepartment))}
            subtitle="평균 학생 수"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="최대 학과"
            value={largestDepartment || '-'}
            subtitle="학생 수 최다"
          />
        </Grid>
      </Grid>
    </Box>
  );
};
