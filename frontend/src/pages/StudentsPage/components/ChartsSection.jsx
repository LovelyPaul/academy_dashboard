/**
 * ChartsSection: Display all chart visualizations for student data
 * Shows department bar chart, grade pie chart, and enrollment trend line chart
 */
import React from 'react';
import { Grid, Paper, Typography, Box, Alert, Button } from '@mui/material';
import { useStudentsAnalysis } from '../../../contexts/StudentsAnalysisContext';
import { BarChart } from '../../../components/charts/BarChart';
import { PieChart } from '../../../components/charts/PieChart';
import { LineChart } from '../../../components/charts/LineChart';
import { Loading } from '../../../components/common/Loading';
import {
  transformToBarChartData,
  transformToPieChartData,
  transformToMultiDatasetChart
} from '../../../services/dataTransformer';

export const ChartsSection = () => {
  const { state, retryFetch } = useStudentsAnalysis();

  if (state.loading) {
    return <Loading />;
  }

  if (state.error) {
    return (
      <Box sx={{ my: 3 }}>
        <Alert
          severity="error"
          action={
            <Button color="inherit" size="small" onClick={retryFetch}>
              재시도
            </Button>
          }
        >
          데이터를 불러오는 중 오류가 발생했습니다: {state.error.message}
        </Alert>
      </Box>
    );
  }

  if (state.departmentStats.length === 0) {
    return (
      <Box sx={{ my: 3 }}>
        <Alert severity="info">
          조회된 학생 데이터가 없습니다. 필터를 초기화하거나 다른 조건으로 조회해보세요.
        </Alert>
      </Box>
    );
  }

  // Transform data for charts
  const departmentChartData = transformToBarChartData(
    state.departmentStats,
    'department',
    'count',
    {
      label: '학생 수',
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
    }
  );

  // Transform grade data - use grade number for labels
  const gradeDataWithLabels = state.gradeDistribution.map(item => ({
    ...item,
    label: item.grade === 0 ? '대학원' : `${item.grade}학년`
  }));

  const gradeChartData = transformToPieChartData(
    gradeDataWithLabels,
    'label',
    'count'
  );

  // Transform enrollment trend data with multiple datasets
  const trendChartData = transformToMultiDatasetChart(
    state.enrollmentTrend,
    'admission_year',
    ['total', 'enrolled'],
    'line'
  );

  // Update dataset labels to Korean
  if (trendChartData.datasets.length >= 2) {
    trendChartData.datasets[0].label = '전체 학생';
    trendChartData.datasets[1].label = '재학생';
  }

  return (
    <Box sx={{ my: 3 }}>
      <Grid container spacing={3}>
        {/* Department Bar Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              학과별 학생 수
            </Typography>
            <Box sx={{ height: 'calc(100% - 40px)' }}>
              <BarChart
                data={departmentChartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { display: false },
                    title: { display: false }
                  },
                  scales: {
                    y: { beginAtZero: true }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Grade Pie Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              학년별 분포
            </Typography>
            <Box sx={{ height: 'calc(100% - 40px)' }}>
              <PieChart
                data={gradeChartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { position: 'right' }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Enrollment Trend Line Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              입학/졸업 추이
            </Typography>
            <Box sx={{ height: 'calc(100% - 40px)' }}>
              <LineChart
                data={trendChartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { position: 'top' }
                  },
                  scales: {
                    y: { beginAtZero: true }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
