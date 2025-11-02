/**
 * Filter Section Component
 * Provides filter controls for year, journal grade, and field
 */
import React from 'react';
import { Grid, FormControl, InputLabel, Select, MenuItem, Button } from '@mui/material';
import { usePapersContext } from '../PapersContext';

export function FilterSection() {
  const { state, setFilter, clearFilters } = usePapersContext();
  const { filters } = state;

  const handleYearChange = (event) => {
    setFilter('year', event.target.value || null);
  };

  const handleJournalChange = (event) => {
    setFilter('journal', event.target.value || null);
  };

  const handleFieldChange = (event) => {
    setFilter('field', event.target.value || null);
  };

  const hasActiveFilters = Object.values(filters).some(v => v !== null);

  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      <Grid item xs={12} sm={3}>
        <FormControl fullWidth>
          <InputLabel>Year</InputLabel>
          <Select
            value={filters.year || ''}
            onChange={handleYearChange}
            label="Year"
          >
            <MenuItem value="">All Years</MenuItem>
            <MenuItem value={2023}>2023</MenuItem>
            <MenuItem value={2022}>2022</MenuItem>
            <MenuItem value={2021}>2021</MenuItem>
            <MenuItem value={2020}>2020</MenuItem>
          </Select>
        </FormControl>
      </Grid>

      <Grid item xs={12} sm={3}>
        <FormControl fullWidth>
          <InputLabel>Journal Grade</InputLabel>
          <Select
            value={filters.journal || ''}
            onChange={handleJournalChange}
            label="Journal Grade"
          >
            <MenuItem value="">All Grades</MenuItem>
            <MenuItem value="SCI">SCI</MenuItem>
            <MenuItem value="KCI">KCI</MenuItem>
            <MenuItem value="SCOPUS">SCOPUS</MenuItem>
            <MenuItem value="기타">기타</MenuItem>
          </Select>
        </FormControl>
      </Grid>

      <Grid item xs={12} sm={3}>
        <FormControl fullWidth>
          <InputLabel>Field</InputLabel>
          <Select
            value={filters.field || ''}
            onChange={handleFieldChange}
            label="Field"
          >
            <MenuItem value="">All Fields</MenuItem>
            <MenuItem value="공학">공학</MenuItem>
            <MenuItem value="의학">의학</MenuItem>
            <MenuItem value="자연과학">자연과학</MenuItem>
            <MenuItem value="인문학">인문학</MenuItem>
          </Select>
        </FormControl>
      </Grid>

      <Grid item xs={12} sm={3}>
        <Button
          variant="outlined"
          fullWidth
          onClick={clearFilters}
          disabled={!hasActiveFilters}
          sx={{ height: '56px' }}
        >
          Clear Filters
        </Button>
      </Grid>
    </Grid>
  );
}

export default FilterSection;
