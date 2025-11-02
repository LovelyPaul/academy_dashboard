/**
 * Sign Up Page Component
 * Use Case 001: Sign Up
 *
 * Integrates Clerk SignUp component for user registration.
 * Handles email verification and user account creation.
 * Backend synchronizes user data via Clerk webhook (user.created event).
 *
 * @module pages/SignUpPage
 * @requires @clerk/clerk-react
 * @requires react-router-dom
 * @requires @mui/material
 * @requires ../layouts/AuthLayout
 */
import React from 'react';
import { SignUp, useUser } from '@clerk/clerk-react';
import { Navigate } from 'react-router-dom';
import { Box, Typography, Link as MuiLink } from '@mui/material';
import { AuthLayout } from '../layouts/AuthLayout';

/**
 * Sign Up Page
 *
 * Displays Clerk SignUp component and handles user registration flow.
 * Automatically redirects authenticated users to the dashboard.
 *
 * Features:
 * - Email/password registration via Clerk
 * - Email verification enforcement
 * - Automatic backend synchronization via webhook
 * - Link to sign-in page for existing users
 * - Responsive design with MUI theme
 *
 * User Flow:
 * 1. User navigates to /sign-up
 * 2. SignUp component is rendered
 * 3. User enters email, password, and optional name
 * 4. Clerk validates input and creates account
 * 5. Clerk sends email verification link
 * 6. User clicks verification link in email
 * 7. Clerk webhook notifies backend (user.created event)
 * 8. Backend creates User record in PostgreSQL with default 'user' role
 * 9. User is redirected to sign-in page
 * 10. User can now log in with credentials
 *
 * Edge Cases Handled:
 * - Duplicate email: Clerk displays error message
 * - Invalid email format: Inline validation error
 * - Weak password: Password strength requirements shown
 * - Password mismatch: Validation error displayed
 * - Network error: Clerk handles retry mechanism
 * - Already authenticated: automatic redirect to dashboard
 * - Email verification not completed: login prevented until verified
 * - Webhook delivery failure: Clerk retries with exponential backoff
 *
 * Security:
 * - All authentication handled by Clerk (battle-tested infrastructure)
 * - Passwords never stored in our backend
 * - JWT tokens for session management
 * - Webhook signatures verified using Svix
 * - HTTPS required for all communications
 *
 * Backend Integration:
 * - Webhook endpoint: /api/webhooks/clerk/
 * - Event: user.created
 * - Handler: UserWebhookUseCase.handle_event()
 * - User creation: UserService.create_user_from_clerk()
 * - Database: User model with clerk_id, email, role='user'
 *
 * @returns {JSX.Element} Sign up page component
 */
const SignUpPage = () => {
  const { isSignedIn, isLoaded } = useUser();

  // Redirect authenticated users to dashboard
  if (isLoaded && isSignedIn) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <AuthLayout title="Create Account">
      <Box sx={{ width: '100%', maxWidth: 400 }}>
        <Typography
          variant="body1"
          color="text.secondary"
          align="center"
          sx={{ mb: 3 }}
        >
          Sign up to access the university data visualization dashboard
        </Typography>

        <SignUp
          path="/sign-up"
          routing="path"
          signInUrl="/sign-in"
          afterSignUpUrl="/sign-in"
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
            Already have an account?{' '}
            <MuiLink href="/sign-in" underline="hover" sx={{ fontWeight: 'medium' }}>
              Sign in here
            </MuiLink>
          </Typography>
        </Box>
      </Box>
    </AuthLayout>
  );
};

export default SignUpPage;
