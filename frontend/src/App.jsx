/**
 * Main App component with routing.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SignedIn, SignedOut } from '@clerk/clerk-react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './styles/theme';

// Import pages
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import PerformancePage from './pages/PerformancePage';
import StudentsPage from './pages/StudentsPage';

// Import layouts (will be used when pages are created)
// import { MainLayout } from './layouts/MainLayout';
// import { AuthLayout } from './layouts/AuthLayout';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          {/* Routes will be added here during page development */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <SignedIn>
                <div>Dashboard Page (To be implemented)</div>
              </SignedIn>
            }
          />
          <Route
            path="/dashboard/performance"
            element={
              <SignedIn>
                <PerformancePage />
              </SignedIn>
            }
          />
          <Route
            path="/dashboard/students"
            element={
              <SignedIn>
                <StudentsPage />
              </SignedIn>
            }
          />

          {/* Public Routes */}
          <Route
            path="/sign-in"
            element={
              <SignedOut>
                <LoginPage />
              </SignedOut>
            }
          />
          <Route
            path="/sign-up"
            element={
              <SignedOut>
                <SignUpPage />
              </SignedOut>
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
