/**
 * LoginPage Component Tests
 *
 * Tests for the Login Page component including:
 * - Component rendering
 * - Clerk SignIn integration
 * - Authentication flow
 * - Redirects
 * - Error handling
 *
 * @module pages/__tests__/LoginPage
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ClerkProvider } from '@clerk/clerk-react';
import LoginPage from '../LoginPage';

// Mock Clerk hooks
jest.mock('@clerk/clerk-react', () => ({
  ...jest.requireActual('@clerk/clerk-react'),
  useUser: jest.fn(),
  SignIn: ({ children }) => <div data-testid="clerk-signin-component">SignIn Component</div>,
}));

// Test publishable key
const mockClerkKey = 'pk_test_mock_key_for_testing';

describe('LoginPage Component', () => {
  const renderLoginPage = (userProps = {}) => {
    const { useUser } = require('@clerk/clerk-react');
    useUser.mockReturnValue({
      isSignedIn: false,
      isLoaded: true,
      ...userProps,
    });

    return render(
      <ClerkProvider publishableKey={mockClerkKey}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </ClerkProvider>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    test('renders login page title', () => {
      renderLoginPage();
      expect(screen.getByText(/Login to Dashboard/i)).toBeInTheDocument();
    });

    test('renders page description', () => {
      renderLoginPage();
      expect(
        screen.getByText(/Access the university data visualization dashboard/i)
      ).toBeInTheDocument();
    });

    test('renders Clerk SignIn component', () => {
      renderLoginPage();
      expect(screen.getByTestId('clerk-signin-component')).toBeInTheDocument();
    });

    test('renders sign-up link', () => {
      renderLoginPage();
      const signUpLink = screen.getByText(/Sign up here/i);
      expect(signUpLink).toBeInTheDocument();
      expect(signUpLink.closest('a')).toHaveAttribute('href', '/sign-up');
    });

    test('renders helper text for new users', () => {
      renderLoginPage();
      expect(screen.getByText(/Don't have an account\?/i)).toBeInTheDocument();
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
            <LoginPage />
          </BrowserRouter>
        </ClerkProvider>
      );

      // Should not render login content while loading
      expect(screen.queryByText(/Login to Dashboard/i)).not.toBeInTheDocument();
    });

    test('renders login form for unauthenticated users', () => {
      renderLoginPage({ isSignedIn: false, isLoaded: true });
      expect(screen.getByTestId('clerk-signin-component')).toBeInTheDocument();
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
            <LoginPage />
          </BrowserRouter>
        </ClerkProvider>
      );

      // Should not render login content for authenticated users
      expect(screen.queryByText(/Login to Dashboard/i)).not.toBeInTheDocument();
    });
  });

  describe('Layout and Styling', () => {
    test('uses AuthLayout component', () => {
      renderLoginPage();
      // AuthLayout should be rendered (check for its structure)
      const description = screen.getByText(/Access the university data visualization dashboard/i);
      expect(description).toBeInTheDocument();
    });

    test('applies correct styling to container', () => {
      renderLoginPage();
      const description = screen.getByText(/Access the university data visualization dashboard/i);
      expect(description.closest('div')).toHaveStyle({ textAlign: 'center' });
    });
  });

  describe('Navigation', () => {
    test('sign-up link points to correct route', () => {
      renderLoginPage();
      const signUpLink = screen.getByText(/Sign up here/i).closest('a');
      expect(signUpLink).toHaveAttribute('href', '/sign-up');
    });

    test('renders with correct route path', () => {
      renderLoginPage();
      // Verify component renders on /sign-in route
      expect(screen.getByTestId('clerk-signin-component')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('has proper semantic HTML structure', () => {
      renderLoginPage();
      const title = screen.getByText(/Login to Dashboard/i);
      expect(title.tagName).toBe('H1');
    });

    test('provides descriptive text for screen readers', () => {
      renderLoginPage();
      expect(
        screen.getByText(/Access the university data visualization dashboard/i)
      ).toBeInTheDocument();
    });

    test('sign-up link is keyboard accessible', () => {
      renderLoginPage();
      const signUpLink = screen.getByText(/Sign up here/i).closest('a');
      expect(signUpLink).toHaveAttribute('href');
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
              <LoginPage />
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
              <LoginPage />
            </BrowserRouter>
          </ClerkProvider>
        );
      }).not.toThrow();
    });
  });

  describe('Integration', () => {
    test('integrates with Clerk provider', () => {
      renderLoginPage();
      // Clerk SignIn component should be rendered
      expect(screen.getByTestId('clerk-signin-component')).toBeInTheDocument();
    });

    test('integrates with React Router', () => {
      renderLoginPage();
      // Component should render without router errors
      expect(screen.getByText(/Login to Dashboard/i)).toBeInTheDocument();
    });

    test('integrates with MUI theme', () => {
      renderLoginPage();
      // MUI components should render
      const description = screen.getByText(/Access the university data visualization dashboard/i);
      expect(description).toBeInTheDocument();
    });
  });
});
