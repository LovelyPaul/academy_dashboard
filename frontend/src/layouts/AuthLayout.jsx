/**
 * Auth Layout for login and signup pages.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Box, Container, Paper, Typography } from '@mui/material';

/**
 * Auth Layout for authentication pages.
 * Provides a centered container for login/signup forms.
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Auth page content
 * @param {string} props.title - Page title (optional)
 * @returns {JSX.Element} Auth Layout component
 */
export const AuthLayout = ({ children, title }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {title && (
            <Typography variant="h4" component="h1" gutterBottom>
              {title}
            </Typography>
          )}
          {children}
        </Paper>
      </Container>
    </Box>
  );
};

export default AuthLayout;
