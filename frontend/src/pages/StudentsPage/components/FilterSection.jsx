/**
 * FilterSection: Filter controls for student data filtering
 * Provides dropdowns for department, grade, and year selection
 */
import React from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Paper,
  Grid
} from '@mui/material';
import { useStudentsAnalysis } from '../../../contexts/StudentsAnalysisContext';

export const FilterSection = () => {
  const {
    state,
    setDepartmentFilter,
    setGradeFilter,
    setYearFilter,
    resetFilters,
    departmentOptions,
    gradeOptions,
    yearOptions,
  } = useStudentsAnalysis();

  return (
    <Paper sx={{ p: 2, my: 3 }}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel>학과</InputLabel>
            <Select
              value={state.selectedDepartment || ''}
              onChange={(e) => setDepartmentFilter(e.target.value || null)}
              label="학과"
            >
              <MenuItem value="">전체 학과</MenuItem>
              {departmentOptions.map(dept => (
                <MenuItem key={dept} value={dept}>{dept}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel>학년</InputLabel>
            <Select
              value={state.selectedGrade === null ? '' : state.selectedGrade}
              onChange={(e) => setGradeFilter(e.target.value === '' ? null : Number(e.target.value))}
              label="학년"
            >
              <MenuItem value="">전체 학년</MenuItem>
              {gradeOptions.map(grade => (
                <MenuItem key={grade} value={grade}>
                  {grade === 0 ? '대학원' : `${grade}학년`}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel>연도</InputLabel>
            <Select
              value={state.selectedYear}
              onChange={(e) => setYearFilter(Number(e.target.value))}
              label="연도"
            >
              {yearOptions.map(year => (
                <MenuItem key={year} value={year}>{year}년</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Button
            variant="outlined"
            onClick={resetFilters}
            fullWidth
          >
            필터 초기화
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};
