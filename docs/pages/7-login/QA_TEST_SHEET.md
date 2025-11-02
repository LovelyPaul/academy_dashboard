# QA Test Sheet: Login Page

> **Page**: Login (`/sign-in`)
> **Implementation Date**: 2025-11-02
> **Test Environment**: Development
> **Tester**: _______________

---

## Test Environment Setup

### Prerequisites
- [ ] Frontend server running on http://localhost:3000
- [ ] Backend server running on http://localhost:8000
- [ ] Clerk account configured with valid API keys
- [ ] PostgreSQL database running
- [ ] Test user account created in Clerk
- [ ] Test user email verified

### Environment Variables
- [ ] `REACT_APP_CLERK_PUBLISHABLE_KEY` configured in frontend/.env.local
- [ ] `CLERK_WEBHOOK_SECRET` configured in backend/.env
- [ ] `CLERK_SECRET_KEY` configured in backend/.env

---

## Functional Tests

### Test Case 001: Login with Valid Credentials
- **Priority**: P0 (Critical)
- **Precondition**: User account exists and email is verified
- **Steps**:
  1. Navigate to `http://localhost:3000/sign-in`
  2. Verify page loads correctly
  3. Enter valid email in email field
  4. Enter valid password in password field
  5. Click "Sign In" button
- **Expected Result**:
  - User is authenticated successfully
  - Redirected to `/dashboard`
  - No error messages displayed
  - User session is active
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 002: Login with Invalid Email
- **Priority**: P1 (High)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/sign-in`
  2. Enter non-existent email (e.g., `nonexistent@test.com`)
  3. Enter any password
  4. Click "Sign In" button
- **Expected Result**:
  - Error message displayed: "Invalid email or password" or similar
  - User remains on login page
  - Form fields are cleared or remain editable
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 003: Login with Invalid Password
- **Priority**: P1 (High)
- **Precondition**: User account exists
- **Steps**:
  1. Navigate to `/sign-in`
  2. Enter valid email
  3. Enter incorrect password
  4. Click "Sign In" button
- **Expected Result**:
  - Error message displayed: "Invalid email or password" or similar
  - User remains on login page
  - Password field is cleared
  - Email field retains the entered value
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 004: Login with Unverified Email
- **Priority**: P1 (High)
- **Precondition**: User account exists but email not verified
- **Steps**:
  1. Create a new user account (if needed)
  2. Do not verify email
  3. Navigate to `/sign-in`
  4. Enter unverified email
  5. Enter correct password
  6. Click "Sign In" button
- **Expected Result**:
  - Verification pending message displayed
  - Option to resend verification email shown
  - User cannot proceed to dashboard
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 005: Redirect Already Authenticated User
- **Priority**: P1 (High)
- **Precondition**: User is already logged in
- **Steps**:
  1. Login successfully to `/dashboard`
  2. Navigate directly to `/sign-in` via URL bar
- **Expected Result**:
  - User is immediately redirected to `/dashboard`
  - Login page does not render
  - No flash of login form
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 006: Sign-up Link Navigation
- **Priority**: P2 (Medium)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/sign-in`
  2. Locate "Sign up here" link
  3. Click the link
- **Expected Result**:
  - User is navigated to `/sign-up`
  - Sign-up page is displayed
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 007: Empty Form Submission
- **Priority**: P2 (Medium)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/sign-in`
  2. Leave email and password fields empty
  3. Click "Sign In" button
- **Expected Result**:
  - Validation error messages displayed
  - "Email is required" or similar message
  - "Password is required" or similar message
  - Form is not submitted
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

### Test Case 008: Email Format Validation
- **Priority**: P2 (Medium)
- **Precondition**: None
- **Steps**:
  1. Navigate to `/sign-in`
  2. Enter invalid email format (e.g., `invalidemail`)
  3. Enter any password
  4. Click "Sign In" button
- **Expected Result**:
  - Validation error message: "Invalid email format" or similar
  - Form is not submitted
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

## Security Tests

### Test Case 101: Password Masking
- **Priority**: P1 (High)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Enter password in password field
  3. Verify password is masked
- **Expected Result**:
  - Password characters are hidden (shown as dots or asterisks)
  - Toggle visibility option available (if implemented by Clerk)
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 102: HTTPS Enforcement (Production Only)
- **Priority**: P1 (High)
- **Precondition**: Deployed to production
- **Steps**:
  1. Attempt to access site via HTTP
- **Expected Result**:
  - Automatically redirected to HTTPS
  - Connection is secure
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail [ ] N/A (Dev Environment)

---

### Test Case 103: Session Token Security
- **Priority**: P1 (High)
- **Steps**:
  1. Login successfully
  2. Open browser developer tools
  3. Check Application > Cookies
  4. Verify Clerk session token
- **Expected Result**:
  - Token is HttpOnly (if applicable)
  - Token is Secure (in production)
  - Token is not accessible via JavaScript
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

## Performance Tests

### Test Case 201: Page Load Time
- **Priority**: P2 (Medium)
- **Steps**:
  1. Clear browser cache
  2. Navigate to `/sign-in`
  3. Measure time to fully load
- **Expected Result**:
  - Page loads in < 2 seconds
  - All components render without delay
- **Actual Result**: _______________ seconds
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 202: Authentication Response Time
- **Priority**: P2 (Medium)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Enter valid credentials
  3. Click "Sign In"
  4. Measure time until redirect to dashboard
- **Expected Result**:
  - Authentication completes in < 3 seconds
  - User is redirected promptly
- **Actual Result**: _______________ seconds
- **Status**: [ ] Pass [ ] Fail

---

## UI/UX Tests

### Test Case 301: Responsive Design - Mobile
- **Priority**: P1 (High)
- **Steps**:
  1. Open browser developer tools
  2. Set device to iPhone 12 Pro (390x844)
  3. Navigate to `/sign-in`
- **Expected Result**:
  - Layout adapts to mobile screen
  - All elements are visible and accessible
  - Text is readable without zooming
  - Buttons are easily tappable
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 302: Responsive Design - Tablet
- **Priority**: P2 (Medium)
- **Steps**:
  1. Set device to iPad (768x1024)
  2. Navigate to `/sign-in`
- **Expected Result**:
  - Layout adapts to tablet screen
  - Content is centered and well-proportioned
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 303: Responsive Design - Desktop
- **Priority**: P1 (High)
- **Steps**:
  1. View on desktop browser (1920x1080)
  2. Navigate to `/sign-in`
- **Expected Result**:
  - Login form is centered
  - Appropriate whitespace around form
  - Text is clearly readable
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 304: Visual Consistency
- **Priority**: P2 (Medium)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Compare with design mockups or style guide
- **Expected Result**:
  - Colors match MUI theme (primary: #1976d2)
  - Typography is consistent
  - Spacing follows design system
  - Buttons have correct styling
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 305: Loading States
- **Priority**: P2 (Medium)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Simulate slow network (throttle to 3G)
  3. Enter credentials and submit
- **Expected Result**:
  - Loading indicator shown during authentication
  - Button is disabled during submission
  - User cannot submit form multiple times
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

## Accessibility Tests

### Test Case 401: Keyboard Navigation
- **Priority**: P1 (High)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Use only keyboard (Tab, Shift+Tab, Enter)
  3. Navigate through all elements
  4. Submit form using Enter key
- **Expected Result**:
  - All interactive elements are reachable via Tab
  - Focus indicators are visible
  - Form can be submitted with Enter key
  - Tab order is logical
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 402: Screen Reader Compatibility
- **Priority**: P1 (High)
- **Steps**:
  1. Enable screen reader (VoiceOver on Mac, NVDA on Windows)
  2. Navigate to `/sign-in`
  3. Navigate through page elements
- **Expected Result**:
  - Page title is announced
  - Form labels are read correctly
  - Error messages are announced
  - Button purposes are clear
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 403: Color Contrast
- **Priority**: P2 (Medium)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Use browser extension (e.g., WAVE) to check contrast
- **Expected Result**:
  - All text meets WCAG AA standards (4.5:1 ratio)
  - Error messages have sufficient contrast
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

## Error Handling Tests

### Test Case 501: Network Error
- **Priority**: P2 (Medium)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Disconnect internet or block Clerk API
  3. Enter credentials and submit
- **Expected Result**:
  - Error message displayed: "Network error" or similar
  - Retry option available
  - User can attempt again
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 502: Multiple Failed Login Attempts
- **Priority**: P2 (Medium)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Enter wrong password 5+ times consecutively
- **Expected Result**:
  - Account temporarily locked (handled by Clerk)
  - Message about account lock displayed
  - Password reset option shown
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 503: Session Expiration
- **Priority**: P2 (Medium)
- **Steps**:
  1. Login successfully
  2. Wait for session to expire (or manually invalidate)
  3. Attempt to access protected page
- **Expected Result**:
  - User is redirected to `/sign-in`
  - Message about expired session shown
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

## Integration Tests

### Test Case 601: Clerk Integration
- **Priority**: P0 (Critical)
- **Steps**:
  1. Verify Clerk dashboard configuration
  2. Login with test user
  3. Check Clerk dashboard for login event
- **Expected Result**:
  - Login event recorded in Clerk dashboard
  - User session is active in Clerk
  - JWT token is valid
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

### Test Case 602: Backend Webhook Sync
- **Priority**: P0 (Critical)
- **Steps**:
  1. Create new user in Clerk
  2. Login with new user
  3. Check backend database
- **Expected Result**:
  - User record created in PostgreSQL `users` table
  - `clerk_id` matches Clerk user ID
  - Email is correctly stored
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail
- **SQL Query**: `SELECT * FROM users WHERE clerk_id = 'user_xxxxx';`

---

### Test Case 603: Post-Login Redirect
- **Priority**: P1 (High)
- **Steps**:
  1. Navigate to `/sign-in`
  2. Login successfully
- **Expected Result**:
  - Redirected to `/dashboard`
  - Dashboard page loads
  - User info displayed in header
- **Actual Result**: _______________
- **Status**: [ ] Pass [ ] Fail

---

## Browser Compatibility Tests

### Test Case 701: Chrome
- **Version**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

### Test Case 702: Firefox
- **Version**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

### Test Case 703: Safari
- **Version**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

### Test Case 704: Edge
- **Version**: _______________
- **Status**: [ ] Pass [ ] Fail
- **Notes**: _______________

---

## Summary

### Test Statistics
- **Total Tests**: 30
- **Tests Passed**: _______________
- **Tests Failed**: _______________
- **Tests Skipped**: _______________
- **Pass Rate**: _______________%

### Critical Issues Found
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Recommendations
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Sign-off
- **Tester Name**: _______________
- **Date**: _______________
- **Approval**: [ ] Approved [ ] Needs Revision
- **Comments**: _______________________________________________
