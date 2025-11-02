/**
 * Loading Overlay Component
 * Displays loading spinner during data fetching
 */
import React from 'react';
import { CircularProgress, Backdrop } from '@mui/material';
import { usePapersContext } from '../PapersContext';

export function LoadingOverlay() {
  const { state } = usePapersContext();
  const { isLoading } = state;

  return (
    <Backdrop
      sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={isLoading}
    >
      <CircularProgress color="inherit" />
    </Backdrop>
  );
}
