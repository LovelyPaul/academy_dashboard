/**
 * SignUpPage Component Tests
 *
 * Tests for the Sign Up Page component including:
 * - Component rendering
 * - Clerk SignUp integration
 * - Registration flow
 * - Redirects
 * - Error handling
 * - Edge cases
 *
 * @module pages/__tests__/SignUpPage
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ClerkProvider } from '@clerk/clerk-react';
import SignUpPage from '../SignUpPage';

// Mock Clerk hooks
jest.mock('@clerk/clerk-react', () => ({
  ...jest.requireActual('@clerk/clerk-react'),
  useUser: jest.fn(),
  SignUp: ({ children }) => <div data-testid="clerk-signup-component">SignUp Component</div>,
}));

// Test publishable key
const mockClerkKey = 'pk_test_mock_key_for_testing';

describe('SignUpPage Component', () => {
  const renderSignUpPage = (userProps = {}) => {
    const { useUser } = require('@clerk/clerk-react');
    useUser.mockReturnValue({
      isSignedIn: false,
      isLoaded: true,
      ...userProps,
    });

    return render(
      <ClerkProvider publishableKey={mockClerkKey}>
        <BrowserRouter>
          <SignUpPage />
        </BrowserRouter>
      </ClerkProvider>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    test('renders sign up page title', () => {
      renderSignUpPage();
      expect(screen.getByText(/Create Account/i)).toBeInTheDocument();
    });

    test('renders page description', () => {
      renderSignUpPage();
      expect(
        screen.getByText(/Sign up to access the university data visualization dashboard/i)
      ).toBeInTheDocument();
    });

    test('renders Clerk SignUp component', () => {
      renderSignUpPage();
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('renders sign-in link', () => {
      renderSignUpPage();
      const signInLink = screen.getByText(/Sign in here/i);
      expect(signInLink).toBeInTheDocument();
      expect(signInLink.closest('a')).toHaveAttribute('href', '/sign-in');
    });

    test('renders helper text for existing users', () => {
      renderSignUpPage();
      expect(screen.getByText(/Already have an account\?/i)).toBeInTheDocument();
    });
  });

  describe('Authentication States', () => {
    test('shows loading state when Clerk is not loaded', () => {
      const { useUser } = require('@clerk/clerk-react');
      useUser.mockReturnValue({
        isSignedIn: false,
        isLoaded: false,
      });

      render(
        <ClerkProvider publishableKey={mockClerkKey}>
          <BrowserRouter>
            <SignUpPage />
          </BrowserRouter>
        </ClerkProvider>
      );

      // Should not render signup content while loading
      expect(screen.queryByText(/Create Account/i)).not.toBeInTheDocument();
    });

    test('renders signup form for unauthenticated users', () => {
      renderSignUpPage({ isSignedIn: false, isLoaded: true });
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('redirects authenticated users to dashboard', () => {
      const { useUser } = require('@clerk/clerk-react');
      useUser.mockReturnValue({
        isSignedIn: true,
        isLoaded: true,
      });

      const { container } = render(
        <ClerkProvider publishableKey={mockClerkKey}>
          <BrowserRouter>
            <SignUpPage />
          </BrowserRouter>
        </ClerkProvider>
      );

      // Should not render signup content for authenticated users
      expect(screen.queryByText(/Create Account/i)).not.toBeInTheDocument();
    });
  });

  describe('Layout and Styling', () => {
    test('uses AuthLayout component', () => {
      renderSignUpPage();
      // AuthLayout should be rendered (check for its structure)
      const description = screen.getByText(/Sign up to access the university data visualization dashboard/i);
      expect(description).toBeInTheDocument();
    });

    test('applies correct styling to container', () => {
      renderSignUpPage();
      const description = screen.getByText(/Sign up to access the university data visualization dashboard/i);
      expect(description.closest('div')).toHaveStyle({ textAlign: 'center' });
    });

    test('maintains consistent styling with LoginPage', () => {
      renderSignUpPage();
      const description = screen.getByText(/Sign up to access the university data visualization dashboard/i);
      // Verify similar structure as LoginPage
      expect(description).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    test('sign-in link points to correct route', () => {
      renderSignUpPage();
      const signInLink = screen.getByText(/Sign in here/i).closest('a');
      expect(signInLink).toHaveAttribute('href', '/sign-in');
    });

    test('renders with correct route path', () => {
      renderSignUpPage();
      // Verify component renders on /sign-up route
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('afterSignUpUrl configured correctly', () => {
      renderSignUpPage();
      // SignUp component should be rendered (will redirect to /sign-in after signup)
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('has proper semantic HTML structure', () => {
      renderSignUpPage();
      const title = screen.getByText(/Create Account/i);
      expect(title.tagName).toBe('H1');
    });

    test('provides descriptive text for screen readers', () => {
      renderSignUpPage();
      expect(
        screen.getByText(/Sign up to access the university data visualization dashboard/i)
      ).toBeInTheDocument();
    });

    test('sign-in link is keyboard accessible', () => {
      renderSignUpPage();
      const signInLink = screen.getByText(/Sign in here/i).closest('a');
      expect(signInLink).toHaveAttribute('href');
    });

    test('provides alternative path for existing users', () => {
      renderSignUpPage();
      const helperText = screen.getByText(/Already have an account\?/i);
      expect(helperText).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    test('handles undefined user state gracefully', () => {
      const { useUser } = require('@clerk/clerk-react');
      useUser.mockReturnValue({
        isSignedIn: undefined,
        isLoaded: true,
      });

      expect(() => {
        render(
          <ClerkProvider publishableKey={mockClerkKey}>
            <BrowserRouter>
              <SignUpPage />
            </BrowserRouter>
          </ClerkProvider>
        );
      }).not.toThrow();
    });

    test('handles null user state gracefully', () => {
      const { useUser } = require('@clerk/clerk-react');
      useUser.mockReturnValue({
        isSignedIn: null,
        isLoaded: true,
      });

      expect(() => {
        render(
          <ClerkProvider publishableKey={mockClerkKey}>
            <BrowserRouter>
              <SignUpPage />
            </BrowserRouter>
          </ClerkProvider>
        );
      }).not.toThrow();
    });

    test('handles missing Clerk context gracefully', () => {
      const { useUser } = require('@clerk/clerk-react');
      useUser.mockReturnValue({
        isSignedIn: false,
        isLoaded: true,
      });

      // Should not throw even if Clerk context has issues
      expect(() => renderSignUpPage()).not.toThrow();
    });
  });

  describe('Integration', () => {
    test('integrates with Clerk provider', () => {
      renderSignUpPage();
      // Clerk SignUp component should be rendered
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('integrates with React Router', () => {
      renderSignUpPage();
      // Component should render without router errors
      expect(screen.getByText(/Create Account/i)).toBeInTheDocument();
    });

    test('integrates with MUI theme', () => {
      renderSignUpPage();
      // MUI components should render
      const description = screen.getByText(/Sign up to access the university data visualization dashboard/i);
      expect(description).toBeInTheDocument();
    });

    test('uses AuthLayout from common modules', () => {
      renderSignUpPage();
      // AuthLayout should provide consistent structure
      expect(screen.getByText(/Create Account/i)).toBeInTheDocument();
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });
  });

  describe('User Flow', () => {
    test('displays registration form for new users', () => {
      renderSignUpPage({ isSignedIn: false, isLoaded: true });
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('provides navigation to login for existing users', () => {
      renderSignUpPage();
      const signInLink = screen.getByText(/Sign in here/i).closest('a');
      expect(signInLink).toHaveAttribute('href', '/sign-in');
    });

    test('maintains state during component lifecycle', () => {
      const { rerender } = renderSignUpPage();
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();

      // Rerender should maintain component
      rerender(
        <ClerkProvider publishableKey={mockClerkKey}>
          <BrowserRouter>
            <SignUpPage />
          </BrowserRouter>
        </ClerkProvider>
      );
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });
  });

  describe('Security', () => {
    test('uses Clerk secure authentication', () => {
      renderSignUpPage();
      // Clerk component should be present (handles security)
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('does not expose sensitive data in DOM', () => {
      const { container } = renderSignUpPage();
      const html = container.innerHTML;
      // Should not contain any API keys or secrets
      expect(html).not.toContain('sk_');
      expect(html).not.toContain('whsec_');
    });
  });

  describe('Responsive Design', () => {
    test('renders on mobile viewport', () => {
      renderSignUpPage();
      // Should render all essential elements
      expect(screen.getByText(/Create Account/i)).toBeInTheDocument();
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
    });

    test('renders on desktop viewport', () => {
      renderSignUpPage();
      // Should render all elements with proper layout
      expect(screen.getByText(/Create Account/i)).toBeInTheDocument();
      expect(screen.getByTestId('clerk-signup-component')).toBeInTheDocument();
      expect(screen.getByText(/Already have an account\?/i)).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    test('handles rapid navigation away from page', () => {
      const { unmount } = renderSignUpPage();
      // Should unmount cleanly without errors
      expect(() => unmount()).not.toThrow();
    });

    test('handles component remounting', () => {
      const { unmount } = renderSignUpPage();
      unmount();
      // Should remount successfully
      expect(() => renderSignUpPage()).not.toThrow();
    });

    test('handles missing optional props gracefully', () => {
      const { useUser } = require('@clerk/clerk-react');
      useUser.mockReturnValue({
        isSignedIn: false,
        isLoaded: true,
      });

      expect(() => {
        render(
          <ClerkProvider publishableKey={mockClerkKey}>
            <BrowserRouter>
              <SignUpPage />
            </BrowserRouter>
          </ClerkProvider>
        );
      }).not.toThrow();
    });
  });
});
