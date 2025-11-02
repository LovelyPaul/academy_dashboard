/**
 * Login Page Component
 * Use Case 002: Login
 *
 * Integrates Clerk SignIn component for user authentication.
 * Redirects authenticated users to dashboard.
 *
 * @module pages/LoginPage
 * @requires @clerk/clerk-react
 * @requires react-router-dom
 * @requires @mui/material
 * @requires ../layouts/AuthLayout
 */
import React from 'react';
import { SignIn, useUser } from '@clerk/clerk-react';
import { Navigate } from 'react-router-dom';
import { Box, Typography, Link as MuiLink } from '@mui/material';
import { AuthLayout } from '../layouts/AuthLayout';

/**
 * Login Page
 *
 * Displays Clerk SignIn component and handles authentication flow.
 * Automatically redirects authenticated users to the dashboard.
 *
 * Features:
 * - Email/password authentication via Clerk
 * - Automatic redirect after successful login
 * - Link to sign-up page for new users
 * - Responsive design with MUI theme
 * - Email verification enforcement
 *
 * User Flow:
 * 1. User navigates to /sign-in
 * 2. SignIn component is rendered
 * 3. User enters credentials
 * 4. Clerk validates credentials
 * 5. On success: redirect to /dashboard
 * 6. On failure: display error message
 *
 * Edge Cases:
 * - Invalid credentials: Clerk displays error
 * - Unverified email: Clerk shows verification prompt
 * - Network error: Clerk handles retry
 * - Already authenticated: automatic redirect to dashboard
 *
 * @returns {JSX.Element} Login page component
 */
const LoginPage = () => {
  const { isSignedIn, isLoaded } = useUser();

  // Redirect authenticated users to dashboard
  if (isLoaded && isSignedIn) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <AuthLayout title="Login to Dashboard">
      <Box sx={{ width: '100%', maxWidth: 400 }}>
        <Typography
          variant="body1"
          color="text.secondary"
          align="center"
          sx={{ mb: 3 }}
        >
          Access the university data visualization dashboard
        </Typography>

        <SignIn
          path="/sign-in"
          routing="path"
          signUpUrl="/sign-up"
          afterSignInUrl="/dashboard"
          appearance={{
            elements: {
              formButtonPrimary: {
                backgroundColor: '#1976d2',
                '&:hover': {
                  backgroundColor: '#1565c0',
                },
              },
              card: {
                boxShadow: 'none',
              },
              rootBox: {
                width: '100%',
              },
              formFieldInput: {
                borderColor: '#e0e0e0',
                '&:focus': {
                  borderColor: '#1976d2',
                },
              },
            },
            layout: {
              socialButtonsPlacement: 'bottom',
              socialButtonsVariant: 'iconButton',
            },
          }}
        />

        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Don't have an account?{' '}
            <MuiLink href="/sign-up" underline="hover" sx={{ fontWeight: 'medium' }}>
              Sign up here
            </MuiLink>
          </Typography>
        </Box>
      </Box>
    </AuthLayout>
  );
};

export default LoginPage;
