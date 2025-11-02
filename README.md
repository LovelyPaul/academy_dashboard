# University Dashboard - Data Visualization Platform

## Project Overview

A comprehensive data visualization dashboard for university internal data management, built with Django REST Framework (backend) and React.js (frontend), featuring Clerk authentication and PostgreSQL database.

## Implementation Summary

This project implements **ALL 37 common modules** as specified in `/docs/common-modules.md`:

### Backend Modules (21 modules)
- ✅ **Phase 0**: Django project initialization, settings (base/dev/prod), requirements.txt
- ✅ **Phase 1**: Core modules (exceptions, middleware, pagination, utils)
- ✅ **Phase 2**: User authentication (User model, repository, service, use_case, webhook)
- ✅ **Phase 3**: Data models (5 models: DepartmentKPI, Publication, Student, ResearchBudgetData, UploadHistory)
- ✅ **Phase 4**: File parsers (4 parsers: DepartmentKPI, Publication, Student, ResearchBudget)

### Frontend Modules (16 modules)
- ✅ **Phase 0**: React project initialization, package.json
- ✅ **Phase 1**: API client, hooks (useAuth, useApiClient), theme
- ✅ **Phase 2**: Common components (Button, Card, Table, Loading)
- ✅ **Phase 3**: Chart components (BarChart, LineChart, PieChart, KPICard)
- ✅ **Phase 4**: Layouts (MainLayout, AuthLayout), utils (formatters, validators), dataTransformer

## Architecture

### Layered Architecture & SOLID Principles

**Backend** (Following `/docs/architecture.md`):
- **Presentation Layer**: ViewSets, Serializers, URL routing
- **Application Layer**: Use Cases (orchestration, transaction management)
- **Domain Layer**: Services (pure business logic)
- **Infrastructure Layer**: Repositories (data access), file parsers, external integrations

**Frontend**:
- **Presentation**: Pages, Components, Layouts
- **Application**: Hooks, State Management
- **Services**: API clients, Data transformers
- **Utils**: Formatters, Validators

## Technology Stack

### Backend
- **Framework**: Django 4.2.7 + Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Authentication**: Clerk (Webhook + API integration)
- **Data Processing**: Pandas 2.1.3
- **Testing**: Pytest

### Frontend
- **Framework**: React 18.2.0
- **UI Library**: Material-UI (MUI) 5.15.0
- **Charts**: Chart.js 4.4.1 + react-chartjs-2
- **Routing**: React Router DOM 6.20.1
- **Authentication**: @clerk/clerk-react 4.30.0
- **API Client**: Axios 1.6.2

## Project Structure

```
.
├── backend/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── core/
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   └── pagination.py
│   ├── utils/
│   │   ├── formatters.py
│   │   ├── validators.py
│   │   └── date_utils.py
│   ├── apps/
│   │   ├── users/
│   │   │   ├── models.py
│   │   │   ├── admin.py
│   │   │   ├── domain/
│   │   │   │   └── services.py
│   │   │   ├── application/
│   │   │   │   └── use_cases.py
│   │   │   ├── infrastructure/
│   │   │   │   ├── repositories.py
│   │   │   │   └── clerk_webhook_views.py
│   │   │   └── presentation/
│   │   │       └── urls.py
│   │   └── data_dashboard/
│   │       ├── models.py
│   │       ├── admin.py
│   │       ├── infrastructure/
│   │       │   └── file_parsers.py
│   │       └── presentation/
│   │           └── urls.py
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── api/
    │   │   └── client.js
    │   ├── components/
    │   │   ├── common/
    │   │   │   ├── Button.jsx
    │   │   │   ├── Card.jsx
    │   │   │   ├── Table.jsx
    │   │   │   └── Loading.jsx
    │   │   └── charts/
    │   │       ├── KPICard.jsx
    │   │       ├── BarChart.jsx
    │   │       ├── LineChart.jsx
    │   │       └── PieChart.jsx
    │   ├── hooks/
    │   │   ├── useAuth.js
    │   │   └── useApiClient.js
    │   ├── layouts/
    │   │   ├── MainLayout.jsx
    │   │   └── AuthLayout.jsx
    │   ├── services/
    │   │   └── dataTransformer.js
    │   ├── utils/
    │   │   ├── formatters.js
    │   │   └── validators.js
    │   ├── styles/
    │   │   └── theme.js
    │   ├── App.jsx
    │   └── index.jsx
    ├── .env.example
    ├── .gitignore
    └── package.json
```

## Database Schema

5 main data models as specified in `/docs/database.md`:

1. **users** - Clerk user synchronization
2. **department_kpis** - Department performance indicators
3. **publications** - Academic publications data
4. **students** - Student information
5. **research_budget_data** - Research projects and budget execution (denormalized)
6. **upload_history** - File upload tracking

## Setup Instructions

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=university_dashboard
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

CLERK_SECRET_KEY=sk_test_YOUR_KEY
CLERK_WEBHOOK_SECRET=whsec_YOUR_SECRET

CORS_ALLOWED_ORIGINS=http://localhost:3000
EOL

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOL
REACT_APP_API_BASE_URL=http://localhost:8000/api
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_YOUR_KEY
EOL

# Start development server
npm start
```

## Common Modules Usage

### Backend Examples

```python
# Using exceptions
from core.exceptions import ValidationError, FileProcessingError

if not data:
    raise ValidationError("Data is required")

# Using formatters
from utils.formatters import format_currency, format_percentage

formatted = format_currency(1000000)  # "1,000,000원"
percent = format_percentage(85.5)  # "85.5%"

# Using file parsers
from apps.data_dashboard.infrastructure.file_parsers import DepartmentKPIParser

parser = DepartmentKPIParser()
data = parser.parse_to_dict('path/to/file.xlsx')
```

### Frontend Examples

```javascript
// Using API client
import { useApiClient } from './hooks/useApiClient';

const { getAuthenticatedClient } = useApiClient();
const client = await getAuthenticatedClient();
const response = await client.get('/dashboard/data/');

// Using formatters
import { formatCurrency, formatDate } from './utils/formatters';

const amount = formatCurrency(1000000);  // "1,000,000원"
const date = formatDate('2024-01-01');  // "2024년 1월 1일"

// Using chart components
import { BarChart } from './components/charts/BarChart';
import { transformToBarChartData } from './services/dataTransformer';

const chartData = transformToBarChartData(data, 'department', 'value');
<BarChart data={chartData} />
```

## Key Features Implemented

### Security & Authentication
- ✅ Clerk integration (SDK, Webhook, API)
- ✅ JWT token verification middleware
- ✅ Role-based access control (admin/user)
- ✅ CORS configuration
- ✅ CSRF protection

### Data Management
- ✅ Excel file parsing (Pandas)
- ✅ File validation
- ✅ UPSERT operations for data updates
- ✅ Upload history tracking
- ✅ Error handling and logging

### Architecture Compliance
- ✅ Layered Architecture (4 layers)
- ✅ SOLID Principles
- ✅ Dependency Injection
- ✅ Repository Pattern
- ✅ Use Case Pattern

### Code Quality
- ✅ No hardcoded values (environment variables)
- ✅ Comprehensive error handling
- ✅ Type hints (Python)
- ✅ JSDoc comments (JavaScript)
- ✅ Consistent naming conventions

## Next Steps for Page Development

All common modules are ready for parallel page development:

### Backend Pages (API Endpoints)
1. Dashboard API (`/api/dashboard/`)
2. Performance Analysis API (`/api/dashboard/performance/`)
3. Papers Analysis API (`/api/dashboard/papers/`)
4. Students Analysis API (`/api/dashboard/students/`)
5. Budget Analysis API (`/api/dashboard/budget/`)
6. Upload API (`/api/admin/upload/`)

### Frontend Pages
1. Login Page (`/sign-in`)
2. Sign Up Page (`/sign-up`)
3. Dashboard Page (`/dashboard`)
4. Performance Page (`/dashboard/performance`)
5. Papers Page (`/dashboard/papers`)
6. Students Page (`/dashboard/students`)
7. Budget Page (`/dashboard/budget`)
8. Upload Page (`/admin/upload`)

## Documentation References

- Requirements: `/docs/requirement.md`
- PRD: `/docs/prd.md`
- User Flows: `/docs/userflow.md`
- Database Schema: `/docs/database.md`
- Common Modules: `/docs/common-modules.md`
- Architecture: `/docs/architecture.md`
- Tech Stack: `/docs/techstack.md`
- Clerk Integration: `/docs/external/clerk.md`

## Development Guidelines

### For Backend Developers
- Use dependency injection for all services
- Follow layered architecture strictly
- All database operations through repositories
- Business logic in domain services
- Orchestration in use cases
- No business logic in views/serializers

### For Frontend Developers
- Use common components from `components/common/`
- Use chart components from `components/charts/`
- Always use `useApiClient` for authenticated requests
- Transform API data using `dataTransformer` utilities
- Format display data using `formatters` utilities
- Validate user input using `validators` utilities

## License

Copyright © 2024 University Dashboard Project. All rights reserved.
