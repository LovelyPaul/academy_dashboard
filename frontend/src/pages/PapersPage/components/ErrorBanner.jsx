/**
 * Error Banner Component
 * Displays error messages with retry button
 */
import React from 'react';
import { Alert, Button, Box } from '@mui/material';
import { usePapersContext } from '../PapersContext';

export function ErrorBanner() {
  const { state, resetError, refetchData } = usePapersContext();
  const { error } = state;

  if (!error) {
    return null;
  }

  const handleRetry = () => {
    resetError();
    refetchData();
  };

  return (
    <Box sx={{ mb: 3 }}>
      <Alert
        severity="error"
        action={
          error.code !== '401' && (
            <Button color="inherit" size="small" onClick={handleRetry}>
              Retry
            </Button>
          )
        }
      >
        {error.message}
      </Alert>
    </Box>
  );
}

export default ErrorBanner;
