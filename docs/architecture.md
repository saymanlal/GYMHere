# System Architecture

## Overview

The Gym Management System follows a modern, scalable architecture with clear separation of concerns.

## Architecture Pattern

**Pattern**: Three-tier architecture with API-first design

```
┌─────────────────────────────────────────────────────┐
│                  Client Layer                        │
│                                                      │
│  Next.js 14 (App Router) + TypeScript + TailwindCSS │
│  - Server Components for SEO & performance          │
│  - Client Components for interactivity              │
│  - ShadCN UI for consistent design                  │
└──────────────────────┬───────────────────────────────┘
                       │
                       │ REST API (JSON)
                       │ JWT Authentication
                       │
┌──────────────────────▼───────────────────────────────┐
│                 Application Layer                    │
│                                                      │
│  Django + Django REST Framework                     │
│  - Business logic                                    │
│  - API endpoints                                     │
│  - Authentication & authorization                    │
│  - Data validation                                   │
└──────────────────────┬───────────────────────────────┘
                       │
                       │ ORM (Django Models)
                       │
┌──────────────────────▼───────────────────────────────┐
│                   Data Layer                         │
│                                                      │
│  PostgreSQL (Primary Database)                      │
│  Redis (Caching & Sessions)                         │
└─────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Directory Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth routes group
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/       # Protected routes group
│   │   ├── layout.tsx     # Dashboard layout
│   │   ├── page.tsx       # Dashboard home
│   │   ├── members/
│   │   ├── subscriptions/
│   │   ├── attendance/
│   │   ├── payments/
│   │   ├── trainers/
│   │   └── settings/
│   └── api/               # API route handlers (if needed)
├── components/
│   ├── ui/                # ShadCN UI components
│   ├── forms/             # Form components
│   ├── tables/            # Table components
│   └── charts/            # Chart components
├── features/              # Feature-specific modules
│   ├── members/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   ├── attendance/
│   └── payments/
├── layouts/               # Layout components
│   ├── DashboardLayout.tsx
│   └── AuthLayout.tsx
├── hooks/                 # Shared custom hooks
│   ├── useAuth.ts
│   ├── useApi.ts
│   └── useDebounce.ts
├── services/              # API services
│   ├── api.ts            # Axios instance
│   ├── auth.service.ts
│   ├── members.service.ts
│   └── payments.service.ts
├── utils/                 # Utility functions
│   ├── formatters.ts
│   ├── validators.ts
│   └── constants.ts
└── styles/
    └── globals.css
```

### State Management

- **React Query (TanStack Query)**: Server state management
- **Zustand**: Client-side global state (auth, UI preferences)
- **React Hook Form**: Form state management

### Data Flow

1. User interacts with UI component
2. Component calls service function
3. Service makes API request to backend
4. Response cached in React Query
5. UI updates automatically

## Backend Architecture

### Directory Structure

```
backend/
├── core/                  # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── users/                 # User management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
├── members/               # Member management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services.py        # Business logic
├── subscriptions/         # Membership plans
├── attendance/            # Attendance tracking
├── payments/              # Payment processing
├── trainers/              # Trainer management
├── workouts/              # Workout programs
├── diet/                  # Diet plans
├── inventory/             # Product inventory
├── expenses/              # Expense tracking
├── reports/               # Analytics
└── notifications/         # Notification system
```

### Design Patterns

#### Service Layer Pattern

Business logic separated from views:

```python
# members/services.py
class MemberService:
    @staticmethod
    def create_member(data):
        # Business logic here
        member = Member.objects.create(**data)
        # Send welcome notification
        NotificationService.send_welcome_email(member)
        return member
    
    @staticmethod
    def renew_subscription(member_id, plan_id):
        # Complex renewal logic
        pass
```

#### Repository Pattern

Data access abstraction (when needed for complex queries):

```python
# members/repositories.py
class MemberRepository:
    @staticmethod
    def get_active_members():
        return Member.objects.filter(status='active').select_related('user')
    
    @staticmethod
    def get_expiring_soon(days=7):
        cutoff_date = timezone.now().date() + timedelta(days=days)
        return Member.objects.filter(
            subscription__end_date__lte=cutoff_date,
            subscription__status='active'
        )
```

### API Design

#### RESTful Conventions

```
GET     /api/members/           # List members
POST    /api/members/           # Create member
GET     /api/members/{id}/      # Get member
PUT     /api/members/{id}/      # Update member
PATCH   /api/members/{id}/      # Partial update
DELETE  /api/members/{id}/      # Delete member

# Nested resources
GET     /api/members/{id}/subscriptions/
POST    /api/members/{id}/subscriptions/
GET     /api/members/{id}/attendance/

# Custom actions
POST    /api/members/{id}/renew/
POST    /api/attendance/check-in/
POST    /api/attendance/check-out/
```

#### Response Format

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "John Doe"
  },
  "message": "Member created successfully",
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```

#### Error Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid data provided",
    "details": {
      "email": ["This field is required"]
    }
  }
}
```

## Authentication & Authorization

### JWT Authentication Flow

```
1. User submits credentials
   ↓
2. Backend validates & returns JWT tokens
   {
     "access": "eyJ...",  (15 min expiry)
     "refresh": "eyJ..."  (7 days expiry)
   }
   ↓
3. Frontend stores tokens (httpOnly cookies preferred)
   ↓
4. Frontend sends access token in Authorization header
   Authorization: Bearer eyJ...
   ↓
5. Backend verifies token & processes request
   ↓
6. If access token expired, use refresh token to get new one
```

### Role-Based Access Control (RBAC)

```python
# Roles hierarchy
ADMIN > MANAGER > TRAINER > RECEPTIONIST

# Permissions structure
{
  "members": ["create", "read", "update", "delete"],
  "payments": ["create", "read"],
  "reports": ["read"]
}
```

### Permission Decorator

```python
from users.permissions import permission_required

@permission_required('members.delete')
def delete_member(request, pk):
    # Only users with 'members.delete' permission can access
    pass
```

## Caching Strategy

### Redis Cache Layers

1. **Session Cache**: User sessions and JWT tokens
2. **Data Cache**: Frequently accessed data (plans, settings)
3. **Query Cache**: Expensive database queries
4. **Page Cache**: Static dashboard data

```python
# Example caching
from django.core.cache import cache

def get_membership_plans():
    plans = cache.get('membership_plans')
    if not plans:
        plans = MembershipPlan.objects.filter(is_active=True)
        cache.set('membership_plans', plans, 3600)  # 1 hour
    return plans
```

## Database Design Principles

### Normalization

- Third Normal Form (3NF) for transactional data
- Denormalization for reporting tables (future optimization)

### Indexing Strategy

- Primary keys (UUID) for security
- Foreign keys for relationships
- Status and date fields for filtering
- Composite indexes for common queries

### Data Integrity

- Foreign key constraints
- Check constraints for business rules
- Triggers for audit logging (via Django signals)

## Performance Optimization

### Backend

1. **Database Query Optimization**
   - Use `select_related()` for foreign keys
   - Use `prefetch_related()` for many-to-many
   - Annotate instead of Python loops
   - Database indexes on filtered fields

2. **API Response Optimization**
   - Pagination on all list endpoints
   - Field filtering (sparse fieldsets)
   - Response compression

3. **Caching**
   - Redis for session and data caching
   - Query result caching
   - Template fragment caching

### Frontend

1. **Next.js Optimizations**
   - Server Components for static content
   - Dynamic imports for code splitting
   - Image optimization with next/image
   - Font optimization

2. **Data Fetching**
   - React Query for caching
   - Debouncing search inputs
   - Infinite scroll for large lists
   - Optimistic updates

## Security Measures

### Backend Security

- SQL injection prevention (Django ORM)
- XSS protection (DRF serializers)
- CSRF protection
- Rate limiting on API endpoints
- Password hashing (bcrypt/argon2)
- Input validation and sanitization
- Secure headers (CORS, CSP)

### Frontend Security

- HttpOnly cookies for tokens
- XSS prevention (React auto-escaping)
- CSRF token handling
- Input sanitization
- Secure API communication (HTTPS only)

## Scalability Considerations

### Horizontal Scaling

- Stateless API design
- Session storage in Redis (shared across instances)
- Database connection pooling
- Load balancer ready

### Vertical Scaling

- Database query optimization
- Efficient indexing
- Caching layers
- Background jobs for heavy tasks

### Future Enhancements

- Database read replicas
- CDN for static assets
- Message queue for async tasks (Celery + RabbitMQ)
- Microservices for specific modules

## Monitoring & Logging

### Logging Strategy

```python
import logging

logger = logging.getLogger(__name__)

# Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.info(f"Member {member_id} subscription renewed")
logger.error(f"Payment failed for invoice {invoice_id}", exc_info=True)
```

### Metrics to Track

- API response times
- Database query performance
- Cache hit/miss ratios
- Error rates
- User activity

## Testing Strategy

### Backend Testing

- **Unit Tests**: Models, serializers, services
- **Integration Tests**: API endpoints
- **Test Coverage**: Minimum 80%

```python
# Example test
from django.test import TestCase

class MemberTestCase(TestCase):
    def test_create_member(self):
        member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        self.assertEqual(member.status, 'active')
```

### Frontend Testing

- **Unit Tests**: Utility functions, hooks
- **Component Tests**: React Testing Library
- **E2E Tests**: Playwright (optional)

## Deployment Architecture

### Docker Containers

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Frontend   │  │   Backend   │  │   Database  │
│  (Next.js)  │  │  (Django)   │  │ (PostgreSQL)│
│   :3000     │  │   :8000     │  │   :5432     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────┬───────┴────────┬───────┘
                │                │
         ┌──────▼────────┐  ┌────▼─────┐
         │  Nginx Proxy  │  │  Redis   │
         │    :80/443    │  │  :6379   │
         └───────────────┘  └──────────┘
```

### Environment Management

- **Development**: Local Docker Compose
- **Staging**: Cloud hosting (AWS/Azure/GCP)
- **Production**: Managed services (RDS, ElastiCache, etc.)

## Development Workflow

1. **Feature Branch**: Create from `develop`
2. **Development**: Write code + tests
3. **Code Review**: Pull request
4. **CI/CD**: Automated tests
5. **Merge**: To `develop` branch
6. **Deploy**: To staging environment
7. **QA Testing**: Manual verification
8. **Production Deploy**: Merge to `main`

## Documentation Standards

- **Code Comments**: For complex logic only
- **Docstrings**: All functions and classes
- **API Documentation**: Auto-generated from DRF
- **README**: In every module folder
- **Architecture Docs**: Keep updated

## Module Independence

Each Django app is self-contained:
- Own models, serializers, views
- Own URLs configuration
- Own services and business logic
- Minimal dependencies on other apps
- Communication through defined interfaces

This ensures:
- Easy testing
- Independent deployment
- Clear boundaries
- Maintainability