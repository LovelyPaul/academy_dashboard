/**
 * Protected Route Components
 *
 * Provides route-level authentication guards for both public and protected pages.
 *
 * @module components/auth/ProtectedRoute
 * @requires @clerk/clerk-react
 * @requires react-router-dom
 * @requires ../common/Loading
 */
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from '@clerk/clerk-react';
import { Loading } from '../common/Loading';

/**
 * Public Route Component
 *
 * Wrapper for public authentication pages (login, signup).
 * Redirects authenticated users to the dashboard.
 *
 * Purpose:
 * - Prevents authenticated users from accessing login/signup pages
 * - Improves UX by automatic redirection
 * - Centralizes authentication logic
 *
 * Use Cases:
 * - Login page (/sign-in)
 * - Signup page (/sign-up)
 * - Password reset page (future)
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Page content to render
 * @returns {JSX.Element} Protected route or redirect
 *
 * @example
 * <Route
 *   path="/sign-in"
 *   element={
 *     <PublicRoute>
 *       <LoginPage />
 *     </PublicRoute>
 *   }
 * />
 */
export const PublicRoute = ({ children }) => {
  const { isSignedIn, isLoaded } = useUser();

  // Show loading indicator while Clerk is initializing
  if (!isLoaded) {
    return <Loading />;
  }

  // Redirect authenticated users to dashboard
  if (isSignedIn) {
    return <Navigate to="/dashboard" replace />;
  }

  // Render public page for unauthenticated users
  return children;
};

/**
 * Private Route Component
 *
 * Wrapper for protected pages that require authentication.
 * Redirects unauthenticated users to the login page.
 *
 * Purpose:
 * - Enforces authentication requirement
 * - Prevents unauthorized access
 * - Preserves intended destination for post-login redirect
 *
 * Use Cases:
 * - Dashboard pages
 * - Analysis pages
 * - Admin pages
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Page content to render
 * @returns {JSX.Element} Protected route or redirect
 *
 * @example
 * <Route
 *   path="/dashboard"
 *   element={
 *     <PrivateRoute>
 *       <DashboardPage />
 *     </PrivateRoute>
 *   }
 * />
 */
export const PrivateRoute = ({ children }) => {
  const { isSignedIn, isLoaded } = useUser();

  // Show loading indicator while Clerk is initializing
  if (!isLoaded) {
    return <Loading />;
  }

  // Redirect unauthenticated users to login
  if (!isSignedIn) {
    return <Navigate to="/sign-in" replace />;
  }

  // Render protected page for authenticated users
  return children;
};

export default PublicRoute;
