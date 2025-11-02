/**
 * Authentication hook using Clerk.
 * Following the common-modules.md specification.
 */
import { useUser, useAuth as useClerkAuth } from '@clerk/clerk-react';

/**
 * Custom authentication hook wrapping Clerk's useUser and useAuth.
 * Provides centralized access to authentication state and methods.
 *
 * @returns {Object} Authentication state and methods
 * @returns {Object} user - Current user object from Clerk
 * @returns {boolean} isLoaded - Whether Clerk has loaded
 * @returns {boolean} isSignedIn - Whether user is signed in
 * @returns {Function} getToken - Function to get JWT token
 * @returns {Function} signOut - Function to sign out
 */
export const useAuth = () => {
  const { user, isLoaded, isSignedIn } = useUser();
  const { getToken, signOut } = useClerkAuth();

  return {
    user,
    isLoaded,
    isSignedIn,
    getToken,
    signOut,
  };
};

export default useAuth;
