import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Box,
  Typography,
} from '@mui/material';
import { FilterList } from '@mui/icons-material';
import { usePerformanceContext } from '../PerformanceContext';

/**
 * Filter Panel Component
 *
 * Allows users to filter performance data by:
 * - Date range (start/end date)
 * - Department
 * - Project
 */
export default function FilterPanel() {
  const { state, actions } = usePerformanceContext();
  const { filters, loadingState } = state;

  const [localFilters, setLocalFilters] = useState(filters);

  const handleDateChange = (field) => (event) => {
    setLocalFilters({
      ...localFilters,
      [field]: event.target.value
    });
  };

  const handleTextChange = (field) => (event) => {
    setLocalFilters({
      ...localFilters,
      [field]: event.target.value || null
    });
  };

  const handleApply = () => {
    actions.updateFilters(localFilters);
  };

  const handleReset = () => {
    actions.resetFilters();
    // Reset will trigger a re-render with new filter values from context
  };

  // Sync local filters when context filters change (e.g., after reset)
  React.useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  const isFilterActive = () => {
    return filters.department || filters.project;
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <FilterList sx={{ mr: 1 }} />
          <Typography variant="h6">필터</Typography>
        </Box>

        <Grid container spacing={2}>
          {/* Start Date */}
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="시작일"
              type="date"
              value={localFilters.startDate}
              onChange={handleDateChange('startDate')}
              InputLabelProps={{ shrink: true }}
              disabled={loadingState.filter}
            />
          </Grid>

          {/* End Date */}
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="종료일"
              type="date"
              value={localFilters.endDate}
              onChange={handleDateChange('endDate')}
              InputLabelProps={{ shrink: true }}
              disabled={loadingState.filter}
            />
          </Grid>

          {/* Department */}
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="부서 (선택사항)"
              value={localFilters.department || ''}
              onChange={handleTextChange('department')}
              disabled={loadingState.filter}
              placeholder="부서명을 입력하세요"
            />
          </Grid>

          {/* Project */}
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="프로젝트 (선택사항)"
              value={localFilters.project || ''}
              onChange={handleTextChange('project')}
              disabled={loadingState.filter}
              placeholder="프로젝트명을 입력하세요"
            />
          </Grid>
        </Grid>

        {/* Action Buttons */}
        <Box display="flex" justifyContent="flex-end" gap={1} mt={2}>
          <Button
            variant="outlined"
            onClick={handleReset}
            disabled={loadingState.filter || !isFilterActive()}
          >
            초기화
          </Button>
          <Button
            variant="contained"
            startIcon={<FilterList />}
            onClick={handleApply}
            disabled={loadingState.filter}
          >
            {loadingState.filter ? '적용 중...' : '필터 적용'}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
