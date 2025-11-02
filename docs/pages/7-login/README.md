# Login Page - Setup and Usage Guide

> **Page**: Login (`/sign-in`)
> **Status**: ✅ Implemented
> **Last Updated**: 2025-11-02

---

## Quick Start

### Prerequisites

1. Node.js (v18+) and npm installed
2. Clerk account created at https://clerk.com
3. Backend server running (optional for frontend-only testing)

### Setup Steps

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

All required dependencies are already in `package.json`:
- `@clerk/clerk-react` - Clerk authentication SDK
- `@mui/material` - Material-UI components
- `react-router-dom` - Routing

#### 2. Configure Clerk

**Get Clerk API Keys**:
1. Go to https://dashboard.clerk.com
2. Create a new application or select existing
3. Navigate to "API Keys" section
4. Copy your **Publishable Key** (starts with `pk_test_` or `pk_live_`)

**Create Environment File**:
```bash
cd frontend
cp .env.local.example .env.local
```

**Edit `.env.local`**:
```bash
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

#### 3. Configure Clerk Dashboard

**Set up URLs** in Clerk Dashboard → "Paths":
- Sign-in URL: `http://localhost:3000/sign-in`
- Sign-up URL: `http://localhost:3000/sign-up`
- After sign-in URL: `http://localhost:3000/dashboard`

**Enable Email/Password** in Clerk Dashboard → "Email, Phone, Username":
- Enable "Email address"
- Enable "Password"
- Require email verification

#### 4. Start Development Server

```bash
npm start
```

The app will open at http://localhost:3000

#### 5. Test Login

Navigate to http://localhost:3000/sign-in

**Test User Creation**:
1. Click "Sign up here" link
2. Create a test account
3. Verify email
4. Return to login page
5. Login with your credentials

---

## File Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── LoginPage.jsx          # Main login component
│   │   └── __tests__/
│   │       └── LoginPage.test.jsx # Test suite
│   ├── components/
│   │   └── auth/
│   │       └── ProtectedRoute.jsx # Route guards
│   ├── layouts/
│   │   └── AuthLayout.jsx         # Auth page layout (common)
│   ├── hooks/
│   │   └── useAuth.js             # Auth hook (common)
│   └── App.jsx                    # Main app with routes

docs/pages/7-login/
├── plan.md                         # Implementation plan
├── QA_TEST_SHEET.md               # QA checklist
├── IMPLEMENTATION_REPORT.md       # Implementation report
└── README.md                      # This file
```

---

## Usage

### Accessing the Login Page

**Direct URL**:
```
http://localhost:3000/sign-in
```

**Programmatic Navigation**:
```jsx
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate('/sign-in');
```

### User Flow

1. **User visits `/sign-in`**
   - If already authenticated → Redirect to `/dashboard`
   - If not authenticated → Show login form

2. **User enters credentials**
   - Email address
   - Password

3. **User clicks "Sign In"**
   - Clerk validates credentials
   - On success → JWT token issued → Redirect to `/dashboard`
   - On failure → Error message displayed

4. **New users**
   - Click "Sign up here" link
   - Navigate to `/sign-up` (to be implemented)

---

## Component API

### LoginPage

**Location**: `frontend/src/pages/LoginPage.jsx`

**Props**: None (self-contained)

**Features**:
- Clerk SignIn component integration
- Automatic redirect for authenticated users
- Sign-up link
- Responsive design

**Usage**:
```jsx
import LoginPage from './pages/LoginPage';

// In App.jsx or routing
<Route path="/sign-in" element={<LoginPage />} />
```

---

### ProtectedRoute

**Location**: `frontend/src/components/auth/ProtectedRoute.jsx`

**Exports**:
1. `PublicRoute` - For login/signup pages
2. `PrivateRoute` - For protected pages

**PublicRoute Props**:
- `children` - Page component to render

**Usage**:
```jsx
import { PublicRoute } from './components/auth/ProtectedRoute';

<Route
  path="/sign-in"
  element={
    <PublicRoute>
      <LoginPage />
    </PublicRoute>
  }
/>
```

**PrivateRoute Props**:
- `children` - Page component to render

**Usage**:
```jsx
import { PrivateRoute } from './components/auth/ProtectedRoute';

<Route
  path="/dashboard"
  element={
    <PrivateRoute>
      <DashboardPage />
    </PrivateRoute>
  }
/>
```

---

## Testing

### Run Unit Tests

```bash
cd frontend
npm test LoginPage
```

### Run All Tests

```bash
npm test
```

### Test Coverage

```bash
npm test -- --coverage
```

### Manual Testing

Follow the QA test sheet:
- Location: `docs/pages/7-login/QA_TEST_SHEET.md`
- 30+ test cases covering all scenarios

---

## Customization

### Styling

**Change Theme Colors**:

Edit `frontend/src/styles/theme.js`:
```jsx
export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Change this
    },
  },
});
```

**Customize Clerk UI**:

Edit `LoginPage.jsx`:
```jsx
<SignIn
  appearance={{
    elements: {
      formButtonPrimary: {
        backgroundColor: '#your-color',
      },
    },
  }}
/>
```

### Redirect URLs

**Change After-Login Redirect**:

Edit `LoginPage.jsx`:
```jsx
<SignIn
  afterSignInUrl="/your-dashboard" // Change this
/>
```

**Change Programmatic Redirect**:

Edit `LoginPage.jsx`:
```jsx
if (isLoaded && isSignedIn) {
  return <Navigate to="/your-route" replace />;
}
```

---

## Troubleshooting

### Issue: "Missing Clerk Publishable Key"

**Error Message**:
```
Error: Missing Clerk Publishable Key
```

**Solution**:
1. Verify `.env.local` file exists in `frontend/` directory
2. Check `REACT_APP_CLERK_PUBLISHABLE_KEY` is set
3. Restart development server: `npm start`

---

### Issue: Login Button Not Working

**Symptoms**:
- Clicking "Sign In" does nothing
- No error messages

**Solution**:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify Clerk API key is correct
4. Check network tab for failed requests

---

### Issue: Infinite Redirect Loop

**Symptoms**:
- Page keeps redirecting
- Can't access login or dashboard

**Solution**:
1. Clear browser cookies
2. Clear localStorage: `localStorage.clear()`
3. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
4. Verify only one `ClerkProvider` in App.jsx

---

### Issue: User Not Found After Login

**Symptoms**:
- Login succeeds
- User not in database

**Solution**:
1. Verify backend webhook is configured
2. Check Clerk dashboard → Webhooks
3. Ensure webhook URL is correct
4. Check backend logs for errors

---

## Environment Variables

### Frontend (.env.local)

```bash
# Required
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_xxx

# Optional (defaults shown)
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

### Backend (.env)

```bash
# Required for webhook
CLERK_WEBHOOK_SECRET=whsec_xxx
CLERK_SECRET_KEY=sk_live_xxx

# Database
DB_NAME=university_dashboard
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Security Best Practices

### Development

1. ✅ Never commit `.env.local` to git
2. ✅ Use `pk_test_` keys for development
3. ✅ Keep `.gitignore` updated
4. ✅ Use HTTPS for production

### Production

1. ✅ Use `pk_live_` keys
2. ✅ Enable HTTPS enforcement
3. ✅ Set production redirect URLs
4. ✅ Enable rate limiting in Clerk
5. ✅ Configure proper CORS settings

---

## Performance Tips

### Optimization

1. **Code Splitting**: LoginPage is lazy-loaded by default
2. **Bundle Size**: Clerk components are optimized
3. **Caching**: Clerk handles session caching

### Monitoring

Check performance:
```bash
npm run build
npm run analyze # If analyzer is installed
```

---

## Accessibility

### WCAG 2.1 Level AA Compliance

- ✅ Keyboard navigation support
- ✅ Screen reader compatible
- ✅ Color contrast ratios met
- ✅ Focus indicators visible
- ✅ Semantic HTML structure

### Testing Accessibility

**Manual Testing**:
1. Tab through all elements
2. Use screen reader (VoiceOver, NVDA)
3. Check color contrast

**Automated Testing**:
- Use WAVE browser extension
- Run Lighthouse audit

---

## Browser Support

| Browser | Minimum Version | Status |
|---------|----------------|--------|
| Chrome | 90+ | ✅ Supported |
| Firefox | 88+ | ✅ Supported |
| Safari | 14+ | ✅ Supported |
| Edge | 90+ | ✅ Supported |

---

## Integration with Backend

### Webhook Flow

```
Clerk Login Event
  ↓
POST /api/webhooks/clerk/
  ↓
clerk_webhook_views.py
  ↓
UserWebhookUseCase
  ↓
UserService
  ↓
UserRepository
  ↓
PostgreSQL (users table)
```

### Verify Integration

**Check user in database**:
```sql
SELECT * FROM users WHERE clerk_id = 'user_xxxxx';
```

**Check Clerk events**:
1. Go to Clerk Dashboard
2. Click "Logs"
3. Filter by "user" events

---

## Deployment

### Frontend Deployment

```bash
cd frontend
npm run build
# Deploy build/ directory
```

### Environment Variables (Production)

**Set in hosting platform**:
```bash
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_live_xxx
REACT_APP_API_BASE_URL=https://api.yourdomain.com/api
```

### Clerk Configuration (Production)

1. Update redirect URLs to production domain
2. Change webhook URL to production endpoint
3. Use `pk_live_` publishable key
4. Configure email templates

---

## Related Documentation

- **Implementation Plan**: `plan.md`
- **QA Test Sheet**: `QA_TEST_SHEET.md`
- **Implementation Report**: `IMPLEMENTATION_REPORT.md`
- **Clerk Integration Guide**: `/docs/external/clerk.md`
- **Common Modules**: `/docs/common-modules.md`
- **Architecture**: `/docs/architecture.md`

---

## Support

### Getting Help

1. Check troubleshooting section above
2. Review Clerk documentation: https://clerk.com/docs
3. Check project documentation in `/docs`
4. Review code comments in source files

### Reporting Issues

When reporting issues, include:
1. Error message (full text)
2. Browser console output
3. Network tab screenshots
4. Steps to reproduce
5. Environment (dev/prod)

---

## Changelog

### v1.0.0 (2025-11-02)
- ✅ Initial implementation
- ✅ Clerk integration
- ✅ Responsive design
- ✅ Comprehensive tests
- ✅ Documentation complete

---

## License

Part of University Data Visualization Dashboard project.

---

**End of README**
