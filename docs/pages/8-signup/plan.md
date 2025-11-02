# Implementation Plan: Sign Up Page (`/sign-up`)

## Overview

This document provides the implementation plan for the Sign Up page (`/sign-up`) of the university data visualization dashboard. The Sign Up feature is based on Clerk authentication, which handles user registration, email verification, and initial user creation. The backend synchronizes user data through Clerk webhooks.

### Module List

| Module Name | Location | Layer | Description |
|-------------|----------|-------|-------------|
| SignUpPage | `frontend/src/pages/SignUpPage.jsx` | Presentation (FE) | Main signup page component using Clerk's SignUp UI |
| useAuth | `frontend/src/hooks/useAuth.js` | Application (FE) | Custom hook for Clerk authentication state (already exists) |
| AuthLayout | `frontend/src/layouts/AuthLayout.jsx` | Presentation (FE) | Layout wrapper for authentication pages (already exists) |
| UserWebhookUseCase | `backend/apps/users/application/use_cases.py` | Application (BE) | Orchestrates user creation from Clerk webhook (already exists) |
| UserService | `backend/apps/users/domain/services.py` | Domain (BE) | Business logic for user management (already exists) |
| UserRepository | `backend/apps/users/infrastructure/repositories.py` | Infrastructure (BE) | Data access layer for User model (already exists) |
| User Model | `backend/apps/users/models.py` | Infrastructure (BE) | Django User model with Clerk integration (already exists) |
| clerk_webhook_handler | `backend/apps/users/infrastructure/clerk_webhook_views.py` | Infrastructure (BE) | Webhook endpoint for Clerk events (already exists) |

### Key Points

- **Frontend**: Minimal implementation - primarily uses Clerk's pre-built SignUp component
- **Backend**: Already implemented through common modules (webhook handler, use cases, repositories)
- **Integration**: Clerk handles authentication UI, email verification, and user creation
- **Data Flow**: User signs up → Clerk creates account → Webhook notifies backend → Backend creates User record

---

## Diagram: Module Relationships

```mermaid
graph TD
    subgraph "Frontend - Presentation Layer"
        A[SignUpPage.jsx] --> B[AuthLayout.jsx]
        A --> C[Clerk SignUp Component]
        A --> D[useAuth Hook]
    end

    subgraph "Clerk Service"
        C --> E[Clerk API]
        E --> F[Email Verification]
        F --> G[user.created Event]
    end

    subgraph "Backend - Infrastructure Layer"
        G --> H[clerk_webhook_handler]
    end

    subgraph "Backend - Application Layer"
        H --> I[UserWebhookUseCase]
    end

    subgraph "Backend - Domain Layer"
        I --> J[UserService]
    end

    subgraph "Backend - Infrastructure Layer"
        J --> K[UserRepository]
        K --> L[User Model]
        L --> M[(PostgreSQL Database)]
    end

    style A fill:#e1f5ff
    style C fill:#fff4e1
    style E fill:#f0e1ff
    style H fill:#ffe1e1
    style I fill:#e1ffe1
    style J fill:#ffe1f5
    style L fill:#f5e1ff
```

---

## Implementation Plan

### 1. Frontend - SignUpPage Component

**File**: `frontend/src/pages/SignUpPage.jsx`

**Purpose**: Render Clerk's pre-built SignUp component with proper routing and styling.

**Dependencies**:
- `@clerk/clerk-react` (SignUp component)
- `frontend/src/layouts/AuthLayout.jsx` (layout wrapper)
- `react-router-dom` (navigation)

**Implementation Details**:

```jsx
/**
 * Sign Up Page Component
 *
 * Uses Clerk's pre-built SignUp component for user registration.
 * Handles routing to sign-in page and dashboard after successful signup.
 *
 * User Flow:
 * 1. User accesses /sign-up route
 * 2. Clerk SignUp component is rendered
 * 3. User enters email, password, and name
 * 4. Clerk validates input and creates account
 * 5. Clerk sends email verification link
 * 6. User clicks verification link
 * 7. Clerk webhook notifies backend (user.created event)
 * 8. Backend creates User record in database
 * 9. User is redirected to sign-in page
 */

import React from 'react';
import { SignUp } from '@clerk/clerk-react';
import { Box, Typography, Link } from '@mui/material';
import { AuthLayout } from '../layouts/AuthLayout';
import { useNavigate } from 'react-router-dom';

const SignUpPage = () => {
  return (
    <AuthLayout title="회원가입">
      <Box sx={{ width: '100%', maxWidth: 400 }}>
        <SignUp
          path="/sign-up"
          routing="path"
          signInUrl="/sign-in"
          afterSignUpUrl="/sign-in"
          appearance={{
            elements: {
              rootBox: {
                width: '100%',
              },
              card: {
                boxShadow: 'none',
              },
            },
          }}
        />

        {/* Additional Helper Text */}
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="body2" color="textSecondary">
            이미 계정이 있으신가요?{' '}
            <Link href="/sign-in" underline="hover">
              로그인
            </Link>
          </Typography>
        </Box>
      </Box>
    </AuthLayout>
  );
};

export default SignUpPage;
```

**Key Features**:
- Uses Clerk's `SignUp` component with routing configuration
- Sets `signInUrl` for navigation to login page
- Sets `afterSignUpUrl` to redirect to sign-in after successful signup
- Wrapped in `AuthLayout` for consistent UI
- Provides link to sign-in page for existing users
- Custom appearance configuration for consistent styling

**Error Handling**:
- Clerk handles all validation errors (email format, password strength, duplicate emails)
- Network errors are handled by Clerk with automatic retry
- Invalid input shows inline error messages from Clerk

---

### 2. Frontend - App.jsx Route Configuration

**File**: `frontend/src/App.jsx`

**Purpose**: Add route for SignUp page.

**Changes Required**:

```jsx
// Add import
import SignUpPage from './pages/SignUpPage';

// Add route in Routes component
<Route
  path="/sign-up"
  element={
    <SignedOut>
      <SignUpPage />
    </SignedOut>
  }
/>
```

**Key Points**:
- Wrapped in `SignedOut` to prevent signed-in users from accessing
- Uses `path="/sign-up"` to match Clerk's routing configuration
- No additional logic needed - Clerk handles everything

---

### 3. Backend - Webhook Handler (Already Implemented)

**File**: `backend/apps/users/infrastructure/clerk_webhook_views.py`

**Status**: ✅ Already implemented

**Purpose**: Receive and verify Clerk webhook events (user.created, user.updated, user.deleted).

**Key Functions**:
- Verifies webhook signature using Svix
- Extracts event type and data
- Delegates to `UserWebhookUseCase` for processing

**No changes required** - existing implementation handles user.created events for signup.

---

### 4. Backend - UserWebhookUseCase (Already Implemented)

**File**: `backend/apps/users/application/use_cases.py`

**Status**: ✅ Already implemented

**Purpose**: Orchestrate user creation/update/deletion based on Clerk webhook events.

**Key Functions**:
- `handle_event(event_type, event_data)`: Routes events to appropriate handlers
- Extracts clerk_id, email, first_name, last_name from event data
- Calls `UserService` for business logic

**No changes required** - existing implementation handles signup flow.

---

### 5. Backend - UserService (Already Implemented)

**File**: `backend/apps/users/domain/services.py`

**Status**: ✅ Already implemented

**Purpose**: Business logic for user management.

**Key Functions**:
- `create_user_from_clerk()`: Creates new user with default role
- `update_user_from_clerk()`: Updates user information
- `delete_user_from_clerk()`: Soft/hard deletes user

**No changes required** - existing implementation creates users with 'user' role by default.

---

### 6. Backend - UserRepository (Already Implemented)

**File**: `backend/apps/users/infrastructure/repositories.py`

**Status**: ✅ Already implemented

**Purpose**: Data access layer for User model.

**Key Functions**:
- `get_by_clerk_id()`: Retrieve user by Clerk ID
- `create_user()`: Create new user record
- `update_user()`: Update user fields
- `delete_user()`: Delete user record

**No changes required** - existing implementation handles CRUD operations.

---

### 7. Backend - User Model (Already Implemented)

**File**: `backend/apps/users/models.py`

**Status**: ✅ Already implemented

**Purpose**: Django User model with Clerk integration.

**Key Fields**:
- `clerk_id`: Unique identifier from Clerk
- `email`: User email (from AbstractUser)
- `first_name`: User first name (from AbstractUser)
- `last_name`: User last name (from AbstractUser)
- `role`: User role (admin/user) - defaults to 'user'

**No changes required** - existing model supports signup flow.

---

## QA Sheet for SignUpPage Component

### Test Case 1: Successful User Registration

**Test ID**: SIGNUP-001

**Preconditions**:
- User is not logged in
- User has valid email address
- Email is not already registered in system

**Test Steps**:
1. Navigate to `/sign-up`
2. Enter valid email address
3. Enter password (minimum 8 characters)
4. Enter password confirmation (matching password)
5. Enter first name (optional)
6. Enter last name (optional)
7. Click "회원가입" (Sign Up) button
8. Check email inbox for verification link
9. Click verification link in email
10. Verify redirect to sign-in page

**Expected Result**:
- ✅ SignUp form is displayed with all fields
- ✅ Input validation works (email format, password strength)
- ✅ "이메일 인증 안내" message is displayed after submission
- ✅ Verification email is received
- ✅ Clicking verification link completes registration
- ✅ User is redirected to sign-in page
- ✅ User can now log in with credentials
- ✅ Backend User record is created with clerk_id and role='user'

**Pass Criteria**:
- All steps complete without errors
- User can successfully log in after verification

---

### Test Case 2: Duplicate Email Registration

**Test ID**: SIGNUP-002

**Preconditions**:
- User is not logged in
- Email is already registered in system

**Test Steps**:
1. Navigate to `/sign-up`
2. Enter email that already exists
3. Enter valid password
4. Enter password confirmation
5. Click "회원가입" button

**Expected Result**:
- ✅ Error message displayed: "이미 존재하는 계정입니다" or similar
- ✅ No email verification sent
- ✅ User remains on signup page
- ✅ Link to sign-in page is available

**Pass Criteria**:
- Clear error message shown
- User can navigate to sign-in page

---

### Test Case 3: Invalid Email Format

**Test ID**: SIGNUP-003

**Preconditions**:
- User is not logged in

**Test Steps**:
1. Navigate to `/sign-up`
2. Enter invalid email (e.g., "notanemail", "test@", "@example.com")
3. Enter valid password
4. Click "회원가입" button

**Expected Result**:
- ✅ Inline error message shown: "올바른 이메일 형식이 아닙니다" or similar
- ✅ Signup button disabled or prevents submission
- ✅ No API request sent

**Pass Criteria**:
- Validation prevents invalid email submission
- Clear error feedback provided

---

### Test Case 4: Password Mismatch

**Test ID**: SIGNUP-004

**Preconditions**:
- User is not logged in

**Test Steps**:
1. Navigate to `/sign-up`
2. Enter valid email
3. Enter password: "Password123!"
4. Enter password confirmation: "Password456!"
5. Attempt to submit

**Expected Result**:
- ✅ Error message: "비밀번호가 일치하지 않습니다"
- ✅ Cannot proceed with signup
- ✅ Password fields are highlighted

**Pass Criteria**:
- User cannot submit with mismatched passwords
- Clear error message displayed

---

### Test Case 5: Weak Password

**Test ID**: SIGNUP-005

**Preconditions**:
- User is not logged in

**Test Steps**:
1. Navigate to `/sign-up`
2. Enter valid email
3. Enter weak password (e.g., "123", "abc")
4. Attempt to submit

**Expected Result**:
- ✅ Error message about password requirements
- ✅ Password strength indicator (if available)
- ✅ Suggestion for stronger password
- ✅ Cannot proceed until password meets requirements

**Pass Criteria**:
- Weak passwords rejected with clear feedback

---

### Test Case 6: Email Verification Not Completed

**Test ID**: SIGNUP-006

**Preconditions**:
- User has registered but not verified email
- User tries to log in

**Test Steps**:
1. Complete signup process (steps 1-7 from SIGNUP-001)
2. Do NOT click email verification link
3. Navigate to `/sign-in`
4. Enter credentials
5. Attempt to login

**Expected Result**:
- ✅ Login prevented
- ✅ Message: "이메일 인증이 필요합니다"
- ✅ Option to resend verification email
- ✅ Clear instructions provided

**Pass Criteria**:
- Unverified users cannot access system
- Resend verification option available

---

### Test Case 7: Network Error During Signup

**Test ID**: SIGNUP-007

**Preconditions**:
- User is not logged in
- Network connection is unstable

**Test Steps**:
1. Navigate to `/sign-up`
2. Enter valid credentials
3. Simulate network disconnection
4. Click "회원가입" button

**Expected Result**:
- ✅ Loading indicator displayed
- ✅ Timeout after reasonable period
- ✅ Error message: "네트워크 오류가 발생했습니다"
- ✅ Retry option available
- ✅ No partial account created

**Pass Criteria**:
- Graceful error handling
- User can retry after connection restored

---

### Test Case 8: Navigate to Sign-In from Sign-Up

**Test ID**: SIGNUP-008

**Preconditions**:
- User is on signup page

**Test Steps**:
1. Navigate to `/sign-up`
2. Click "이미 계정이 있으신가요? 로그인" link

**Expected Result**:
- ✅ Redirected to `/sign-in`
- ✅ Sign-in page loads correctly
- ✅ No data loss or errors

**Pass Criteria**:
- Navigation works smoothly
- Sign-in page displays properly

---

### Test Case 9: Signed-In User Accessing Signup

**Test ID**: SIGNUP-009

**Preconditions**:
- User is already logged in

**Test Steps**:
1. Log in to application
2. Attempt to navigate to `/sign-up` via URL

**Expected Result**:
- ✅ Redirected to dashboard or prevented from accessing
- ✅ SignUp page not shown
- ✅ No errors in console

**Pass Criteria**:
- Logged-in users cannot access signup page

---

### Test Case 10: Webhook Processing Verification

**Test ID**: SIGNUP-010

**Preconditions**:
- Backend is running
- Clerk webhook is properly configured
- Database is accessible

**Test Steps**:
1. Complete full signup process (including email verification)
2. Check backend logs for webhook event
3. Query database for new User record
4. Verify User fields

**Expected Result**:
- ✅ Backend receives `user.created` webhook event
- ✅ Webhook signature verified successfully
- ✅ UserWebhookUseCase processes event
- ✅ New User record created in database with:
  - clerk_id = [Clerk User ID]
  - email = [User's email]
  - first_name = [User's first name] (if provided)
  - last_name = [User's last name] (if provided)
  - role = 'user' (default)
- ✅ No errors in backend logs
- ✅ Webhook response 200 OK

**Pass Criteria**:
- Complete backend synchronization
- User record matches Clerk data
- Default role assigned correctly

---

## Edge Cases and Error Handling

### Edge Case 1: Email Verification Link Expired

**Scenario**: User clicks verification link after 24 hours

**Handling**:
- Clerk displays error message
- Option to resend verification email
- User must request new verification link

**Implementation**: Handled entirely by Clerk - no custom code needed

---

### Edge Case 2: Webhook Delivery Failure

**Scenario**: Backend is down when Clerk sends user.created webhook

**Handling**:
- Clerk automatically retries webhook (with exponential backoff)
- Backend logs webhook events when received
- If webhook never succeeds, manual user sync may be needed (admin task)

**Implementation**:
- Clerk handles retry logic
- Backend logs all webhook attempts
- Admin dashboard can show users without backend records (future enhancement)

---

### Edge Case 3: Multiple Simultaneous Signups

**Scenario**: Multiple users sign up at exact same time

**Handling**:
- Each signup is independent
- Clerk handles concurrency
- Database constraints prevent duplicate clerk_id
- Webhook processing is sequential per user

**Implementation**: No special handling required - architecture supports concurrent requests

---

### Edge Case 4: Browser Refresh During Signup

**Scenario**: User refreshes page during signup process

**Handling**:
- Clerk maintains state
- If account already created, shows "account exists" error
- If email not verified, shows verification pending state
- User can continue from where they left off

**Implementation**: Clerk handles state management - no custom code needed

---

### Edge Case 5: Special Characters in Name

**Scenario**: User enters name with special characters (accents, unicode)

**Handling**:
- Clerk accepts unicode characters
- Backend stores as UTF-8
- Database supports unicode
- Display correctly in all UIs

**Implementation**:
- Ensure database charset is UTF-8
- No sanitization needed (Clerk handles)

---

## Security Considerations

### 1. Authentication Security
- ✅ Clerk handles password hashing and storage
- ✅ JWT tokens used for session management
- ✅ HTTPS required for all communications
- ✅ CSRF protection via Clerk

### 2. Webhook Security
- ✅ Webhook signatures verified using Svix
- ✅ Webhook secret stored in environment variables
- ✅ Only POST requests accepted
- ✅ Rate limiting can be configured in Clerk dashboard

### 3. Data Privacy
- ✅ Passwords never stored in backend
- ✅ Personal data encrypted in transit
- ✅ Clerk complies with GDPR/PIPA
- ✅ Email verification required before access

### 4. Rate Limiting
- ✅ Clerk provides built-in rate limiting
- ✅ Prevents signup spam
- ✅ Configurable in Clerk dashboard

---

## Dependencies

### Frontend Dependencies (Already Installed)
```json
{
  "@clerk/clerk-react": "^4.x",
  "@mui/material": "^5.x",
  "react": "^18.x",
  "react-router-dom": "^6.x"
}
```

### Backend Dependencies (Already Installed)
```txt
Django>=4.2
djangorestframework>=3.14
svix>=1.x
psycopg2-binary>=2.9
```

### Environment Variables Required

**Frontend** (`frontend/.env`):
```env
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_live_YOUR_KEY_HERE
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

**Backend** (`backend/.env`):
```env
CLERK_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE
CLERK_SECRET_KEY=sk_live_YOUR_KEY_HERE
DATABASE_URL=postgresql://user:password@localhost:5432/university_dashboard
```

---

## Integration Points

### 1. With Clerk Service
- **Signup UI**: Clerk provides pre-built component
- **Email Verification**: Clerk sends and manages verification emails
- **Webhook Events**: Clerk sends user.created event to backend
- **Session Management**: Clerk manages JWT tokens

### 2. With Backend
- **Webhook Endpoint**: `/api/webhooks/clerk/` receives Clerk events
- **User Creation**: Backend creates User record when webhook received
- **Role Assignment**: Backend assigns default 'user' role

### 3. With Frontend Routing
- **SignUp Route**: `/sign-up` displays SignUp component
- **After Signup**: Redirects to `/sign-in` after email verification
- **Protected Routes**: Dashboard accessible only after authentication

---

## Testing Strategy

### Unit Tests
**Not Required** - No business logic in SignUp page component. All logic handled by Clerk and existing backend modules.

### Integration Tests
**Recommended**:
1. Test Clerk webhook to backend integration
2. Test User creation from webhook event
3. Test default role assignment

**Location**: `backend/apps/users/tests/integration/test_webhook_integration.py`

### End-to-End Tests
**Recommended**:
1. Complete signup flow (signup → email verification → login)
2. Duplicate email handling
3. Network error recovery

**Tools**: Playwright, Cypress, or Selenium

### Manual QA
**Required**: Complete QA sheet above (10 test cases)

---

## Deployment Checklist

### Pre-Deployment
- [ ] Verify Clerk webhook endpoint is configured in Clerk dashboard
- [ ] Verify environment variables are set in production
- [ ] Test webhook delivery in Clerk dashboard (Test Webhook feature)
- [ ] Verify database has users table with correct schema
- [ ] Verify frontend can reach backend API

### Post-Deployment
- [ ] Test complete signup flow in production
- [ ] Verify email delivery works
- [ ] Check backend logs for webhook events
- [ ] Verify User records are created correctly
- [ ] Test error scenarios (duplicate email, weak password)

### Monitoring
- [ ] Set up logging for webhook events
- [ ] Monitor webhook success/failure rates
- [ ] Track signup conversion rates
- [ ] Alert on webhook delivery failures

---

## Rollback Plan

### If Frontend Issues
1. Revert SignUpPage.jsx changes
2. Remove `/sign-up` route from App.jsx
3. Deploy previous version

### If Backend Issues
1. Webhook handler is already implemented - no rollback needed
2. If database issues, restore from backup
3. If Clerk issues, contact Clerk support

### If Webhook Issues
1. Check Clerk dashboard for webhook status
2. Verify webhook secret is correct
3. Check backend logs for errors
4. Re-test webhook delivery in Clerk dashboard
5. Manual user sync if needed (admin task)

---

## Future Enhancements

### Phase 2
1. **Custom signup fields**: Add university-specific fields (department, student ID)
2. **Social login**: Add Google, GitHub OAuth options via Clerk
3. **Admin approval**: Require admin approval for new users

### Phase 3
1. **Two-factor authentication**: Enable 2FA via Clerk
2. **Magic link login**: Add passwordless authentication
3. **Signup analytics**: Track signup sources and conversion rates

---

## Conclusion

The Sign Up page implementation is **minimal and straightforward** due to Clerk handling all authentication complexity:

1. **Frontend**: Single component using Clerk's pre-built UI
2. **Backend**: Already implemented via common modules
3. **Integration**: Webhook-based synchronization
4. **Security**: Handled by Clerk
5. **Testing**: Focus on QA sheet and integration tests

**Estimated Implementation Time**:
- Frontend: 1-2 hours (mostly configuration and styling)
- Backend: 0 hours (already implemented)
- Testing: 2-3 hours (QA sheet execution)
- **Total**: 3-5 hours

**Dependencies**: None - all required modules exist

**Risk Level**: Low - Clerk provides battle-tested authentication infrastructure
