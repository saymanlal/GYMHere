# Backend - Gym Management System

Django REST Framework backend with PostgreSQL and Redis.

## Tech Stack

- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: DRF Spectacular (OpenAPI/Swagger)

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional, for caching)

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Create database
createdb gym_management

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## Project Structure

```
backend/
├── core/                   # Project configuration
│   ├── settings/
│   │   ├── base.py        # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py            # Root URL configuration
│   ├── exceptions.py      # Custom exception handlers
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── users/                  # User authentication
│   ├── models.py          # User and Role models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   ├── permissions.py     # Custom permissions
│   ├── signals.py         # Django signals
│   └── admin.py           # Admin configuration
├── members/                # Member management
├── attendance/             # Attendance tracking
├── subscriptions/          # Membership plans
├── payments/               # Payment processing
├── trainers/               # Trainer management
├── workouts/               # Workout programs
├── diet/                   # Diet plans
├── inventory/              # Product inventory
├── expenses/               # Expense tracking
├── reports/                # Analytics and reports
├── notifications/          # Notification system
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Key Features

### JWT Authentication

All authenticated endpoints require a JWT token:

```http
Authorization: Bearer <access_token>
```

Tokens are obtained via `/api/auth/login/` and refreshed via `/api/auth/refresh/`

### Role-Based Access Control (RBAC)

Users have roles with specific permissions:

```python
from users.permissions import permission_required

@permission_required('members', 'delete')
def delete_member(request, pk):
    # Only users with 'members.delete' permission can access
    pass
```

### Consistent API Responses

All endpoints return consistent response format:

```python
from core.exceptions import success_response

return success_response(
    data={'id': 1, 'name': 'John'},
    message='Operation successful',
    status_code=status.HTTP_200_OK
)
```

Response format:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

Error format:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": {...}
  }
}
```

### Pagination

List endpoints are automatically paginated:

```python
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # Pagination settings in REST_FRAMEWORK config
```

### Filtering and Searching

ViewSets support filtering, searching, and ordering:

```python
class MemberViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'gender']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'first_name']
```

## Database Models

### UUID Primary Keys

All models use UUID primary keys for security:

```python
import uuid
from django.db import models

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ... other fields
```

### Timestamps

All models include audit timestamps:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### Indexes

Important fields are indexed for performance:

```python
class Meta:
    indexes = [
        models.Index(fields=['email']),
        models.Index(fields=['status']),
    ]
```

## Django Apps

### Users
- Custom User model with email authentication
- Role-based permissions
- JWT token management

### Members
- Member profiles and management
- Lead tracking and conversion
- Member status (active, inactive, suspended, expired)

### Subscriptions
- Membership plans
- Subscription management
- Auto-renewal tracking

### Attendance
- Member check-in/check-out
- Trainer attendance
- Attendance logs and reports

### Payments
- Payment processing
- Invoice generation
- Payment tracking

### Trainers
- Trainer profiles
- Trainer assignments
- Specializations and certifications

### Workouts
- Workout plan creation
- Exercise library
- Progress tracking

### Diet
- Diet plan management
- Meal planning
- Nutrition tracking

### Inventory
- Product catalog
- Stock management
- Supplement sales

### Expenses
- Expense tracking
- Category management
- Staff salaries

### Reports
- Revenue analytics
- Member growth
- Attendance statistics

### Notifications
- Email notifications
- SMS alerts
- Reminder system

## Management Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Django shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users

# Run with coverage
pytest --cov=. --cov-report=html
```

Example test:

```python
from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass123"))
```

## Admin Panel

Access Django admin at `http://localhost:8000/admin/`

All models are registered with customized admin interfaces for easy management.

## Environment Variables

Required variables in `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=gym_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# Email (production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use strong SECRET_KEY** - Generate with Django's `get_random_secret_key()`
3. **Set DEBUG=False** in production
4. **Use HTTPS** in production
5. **Validate all input data** with serializers
6. **Use parameterized queries** (Django ORM does this automatically)
7. **Implement rate limiting** on API endpoints
8. **Keep dependencies updated**

## Performance Tips

1. **Use `select_related()`** for foreign keys
2. **Use `prefetch_related()`** for many-to-many relationships
3. **Add database indexes** on frequently queried fields
4. **Use Redis caching** for expensive queries
5. **Implement pagination** on all list endpoints
6. **Use database connection pooling** in production

## Deployment

See production deployment guide for:
- Gunicorn/Uvicorn setup
- Nginx configuration
- SSL certificates
- Static file serving
- Database connection pooling
- Environment configuration

## Troubleshooting

**Database Connection Error**
- Check PostgreSQL is running: `pg_isready`
- Verify credentials in `.env`
- Ensure database exists: `createdb gym_management`

**Migration Errors**
- Reset migrations if needed
- Check for circular dependencies
- Use `--merge` flag for conflicts

**Import Errors**
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

**Permission Denied**
- Check user has required role permissions
- Verify authentication token is valid

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)