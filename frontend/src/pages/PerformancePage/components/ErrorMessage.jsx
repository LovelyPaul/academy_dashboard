import React from 'react';
import { Alert, AlertTitle, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { usePerformanceContext } from '../PerformanceContext';

/**
 * Error Message Component
 *
 * Displays error with appropriate recovery actions based on error type
 */
export default function ErrorMessage() {
  const { state, actions } = usePerformanceContext();
  const { error } = state;
  const navigate = useNavigate();

  if (!error) return null;

  const handleRetry = () => {
    actions.clearError();
    actions.fetchPerformanceData();
  };

  const handleLogin = () => {
    navigate('/sign-in');
  };

  const getErrorSeverity = () => {
    return error.type === 'auth' ? 'warning' : 'error';
  };

  const getActionButton = () => {
    if (error.type === 'auth') {
      return (
        <Button color="inherit" size="small" onClick={handleLogin}>
          로그인 페이지로 이동
        </Button>
      );
    }

    return (
      <Button color="inherit" size="small" onClick={handleRetry}>
        재시도
      </Button>
    );
  };

  return (
    <Box mb={3}>
      <Alert
        severity={getErrorSeverity()}
        action={getActionButton()}
      >
        <AlertTitle>오류 발생</AlertTitle>
        {error.message}
      </Alert>
    </Box>
  );
}
