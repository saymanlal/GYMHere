# Developer Guide

## Getting Started

### Prerequisites

Ensure you have the following installed:
- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+
- **Redis** 7+ (optional, for caching)
- **Git**

### Initial Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd gym-management-system
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Create PostgreSQL database
createdb gym_management

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create initial roles (optional)
python manage.py shell
```

In the shell:
```python
from users.models import Role

# Create admin role
Role.objects.create(
    name='admin',
    description='Full system access',
    permissions={
        'members': ['create', 'read', 'update', 'delete'],
        'payments': ['create', 'read', 'update', 'delete'],
        'trainers': ['create', 'read', 'update', 'delete'],
        'reports': ['read'],
        'settings': ['read', 'update']
    }
)

# Create manager role
Role.objects.create(
    name='manager',
    description='Manage gym operations',
    permissions={
        'members': ['create', 'read', 'update'],
        'payments': ['create', 'read'],
        'trainers': ['read'],
        'reports': ['read']
    }
)

# Create receptionist role
Role.objects.create(
    name='receptionist',
    description='Front desk operations',
    permissions={
        'members': ['create', 'read', 'update'],
        'payments': ['create', 'read'],
        'attendance': ['create', 'read']
    }
)

exit()
```

```bash
# Start development server
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Project Structure

### Backend Structure

```
backend/
├── core/                   # Project settings
│   ├── settings/
│   │   ├── base.py        # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py            # Root URL configuration
│   └── exceptions.py      # Custom exception handlers
├── users/                  # User authentication
│   ├── models.py          # User and Role models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   ├── permissions.py     # Custom permissions
│   └── signals.py         # Django signals
├── members/                # Member management
│   ├── models.py          # Member and Lead models
│   ├── serializers.py     # Serializers
│   ├── views.py           # ViewSets
│   ├── urls.py            # Routing
│   ├── signals.py         # Signals
│   └── admin.py           # Admin configuration
└── [other apps...]
```

### Frontend Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth routes (login, register)
│   ├── (dashboard)/       # Protected dashboard routes
│   │   ├── members/       # Members pages
│   │   ├── payments/      # Payments pages
│   │   └── ...
│   └── layout.tsx         # Root layout
├── components/
│   ├── ui/                # Reusable UI components (Button, Card, etc.)
│   ├── forms/             # Form components
│   └── layouts/           # Layout components
├── features/              # Feature modules
│   ├── members/
│   │   ├── components/    # Member-specific components
│   │   ├── hooks/         # Custom hooks (React Query)
│   │   ├── services/      # API service calls
│   │   └── types.ts       # TypeScript types
│   └── [other features...]
├── hooks/                 # Shared hooks
├── services/              # API configuration
│   ├── api.ts            # Axios instance & interceptors
│   └── auth.service.ts   # Auth service
├── utils/                 # Utility functions
│   └── helpers.ts        # Helper functions
└── styles/
    └── globals.css       # Global styles
```

## Development Workflow

### Creating a New Feature Module

#### Backend

1. **Create Django App**
```bash
cd backend
python manage.py startapp feature_name
```

2. **Add to INSTALLED_APPS** in `core/settings/base.py`

3. **Create Models** in `feature_name/models.py`
```python
import uuid
from django.db import models

class YourModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'your_table_name'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

4. **Create Serializers** in `feature_name/serializers.py`
```python
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
```

5. **Create Views** in `feature_name/views.py`
```python
from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer
from core.exceptions import success_response

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
```

6. **Create URLs** in `feature_name/urls.py`
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.YourModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

7. **Register in Root URLs** in `core/urls.py`
```python
urlpatterns = [
    # ...
    path('api/feature/', include('feature_name.urls')),
]
```

8. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Frontend

1. **Create Feature Directory**
```bash
mkdir -p features/feature_name/{components,hooks,services}
```

2. **Create Types** in `features/feature_name/types.ts`
```typescript
export interface YourModel {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateYourModelData {
  name: string;
}
```

3. **Create Service** in `features/feature_name/services/your-model.service.ts`
```typescript
import { apiService, ApiResponse } from "@/services/api";
import { YourModel, CreateYourModelData } from "../types";

class YourModelService {
  async getAll(): Promise<YourModel[]> {
    const response = await apiService.get<ApiResponse<YourModel[]>>("/feature/");
    return response.data;
  }
  
  async create(data: CreateYourModelData): Promise<YourModel> {
    const response = await apiService.post<ApiResponse<YourModel>>("/feature/", data);
    return response.data;
  }
}

export const yourModelService = new YourModelService();
```

4. **Create Hooks** in `features/feature_name/hooks/useYourModelQueries.ts`
```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { yourModelService } from "../services/your-model.service";

export function useYourModels() {
  return useQuery({
    queryKey: ["your-models"],
    queryFn: () => yourModelService.getAll(),
  });
}

export function useCreateYourModel() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: yourModelService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["your-models"] });
    },
  });
}
```

5. **Create Page** in `app/(dashboard)/feature/page.tsx`
```typescript
"use client";

import { useYourModels } from "@/features/feature_name/hooks/useYourModelQueries";

export default function FeaturePage() {
  const { data, isLoading } = useYourModels();
  
  return (
    <div>
      <h1>Your Feature</h1>
      {/* Your component JSX */}
    </div>
  );
}
```

## Code Standards

### Backend (Python/Django)

- **PEP 8**: Follow Python style guide
- **Type Hints**: Use type hints where applicable
- **Docstrings**: Document all classes and functions
- **Imports**: Organize imports (standard library, third-party, local)

```python
"""
Module docstring explaining purpose
"""
from typing import List, Optional
from django.db import models
from rest_framework import serializers

class Example:
    """
    Class docstring explaining purpose
    """
    def method(self, param: str) -> Optional[str]:
        """
        Method docstring explaining what it does
        
        Args:
            param: Parameter description
            
        Returns:
            Return value description
        """
        return param
```

### Frontend (TypeScript/React)

- **TypeScript**: Use strict types, avoid `any`
- **Components**: Functional components with hooks
- **File naming**: `kebab-case.tsx` for files, `PascalCase` for components
- **Props**: Define interfaces for all component props

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
}

export function Button({ label, onClick, variant = "primary" }: ButtonProps) {
  return (
    <button onClick={onClick} className={`btn-${variant}`}>
      {label}
    </button>
  );
}
```

## Testing

### Backend Tests

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
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
```

### Frontend Tests

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Common Tasks

### Adding a New API Endpoint

1. Add method to ViewSet (backend)
2. Update URLs if needed
3. Create service method (frontend)
4. Create React Query hook
5. Update types
6. Document in API docs

### Adding a New Permission

1. Add permission to Role model permissions
2. Use `@permission_required` decorator or `HasPermission` class
3. Check permission in frontend before showing UI elements

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate app_name migration_name

# Show migrations
python manage.py showmigrations
```

## Debugging

### Backend Debugging

- Use Django Debug Toolbar (already installed in development)
- Add print statements or use `import pdb; pdb.set_trace()`
- Check logs in console

### Frontend Debugging

- Use React DevTools browser extension
- Use browser console for logging
- React Query DevTools (included)

## Deployment

See separate deployment documentation for production setup.

## Troubleshooting

### Common Issues

**Issue**: Database connection error
**Solution**: Check PostgreSQL is running and credentials in `.env`

**Issue**: CORS errors
**Solution**: Verify `CORS_ALLOWED_ORIGINS` in settings

**Issue**: Module not found errors
**Solution**: Reinstall dependencies (`pip install -r requirements.txt` or `npm install`)

**Issue**: Migration conflicts
**Solution**: Delete migration files and recreate, or use `--merge` flag

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Documentation](https://tanstack.com/query/latest)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

## Getting Help

- Check existing documentation
- Review code examples in similar modules
- Ask team members
- Check Django/Next.js documentation