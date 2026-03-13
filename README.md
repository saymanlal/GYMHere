# Gym Management System

A production-grade, full-stack SaaS platform for comprehensive gym and fitness center management.

## 🏗️ Architecture

**Frontend**: Next.js 14 (App Router) + TypeScript + TailwindCSS + ShadCN UI  
**Backend**: Django + Django REST Framework  
**Database**: PostgreSQL  
**Cache**: Redis  
**Auth**: JWT  
**Deployment**: Docker-ready

## 🎯 Core Features

- **Dashboard & Analytics** - Real-time metrics, revenue tracking, member insights
- **Member Management** - Complete member lifecycle, profiles, history
- **Lead Management** - Enquiry tracking, conversion pipeline
- **Membership Plans** - Flexible plans, subscriptions, renewals
- **Attendance System** - Check-in/out, logs, trainer attendance
- **Payments & Invoicing** - Billing, payment tracking, revenue reports
- **Trainer Management** - Profiles, assignments, schedules
- **Workout Programs** - Custom plans, exercise library
- **Diet Plans** - Nutrition tracking, meal plans
- **Health Tracking** - Weight, measurements, progress charts
- **Supplement Sales** - Inventory, product catalog, sales
- **Expense Management** - Tracking, categories, staff payroll
- **Staff Management** - Roles, permissions, attendance
- **Notifications** - SMS, email, expiry reminders
- **Reports** - Comprehensive analytics and insights
- **Settings** - Gym configuration, role-based access

## 📁 Project Structure

```
gym-management-system/
├── frontend/              # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # Reusable UI components
│   ├── layouts/          # Layout components
│   ├── features/         # Feature-specific modules
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API service layer
│   ├── utils/            # Utility functions
│   └── styles/           # Global styles
├── backend/              # Django application
│   ├── core/             # Core settings and config
│   ├── users/            # User authentication
│   ├── members/          # Member management
│   ├── attendance/       # Attendance tracking
│   ├── subscriptions/    # Membership plans
│   ├── payments/         # Payment processing
│   ├── trainers/         # Trainer management
│   ├── workouts/         # Workout programs
│   ├── diet/             # Diet plans
│   ├── inventory/        # Product inventory
│   ├── expenses/         # Expense tracking
│   ├── reports/          # Analytics and reports
│   └── notifications/    # Notification system
├── database/             # Database documentation
├── docs/                 # Project documentation
└── docker/               # Docker configuration
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Docker Setup

```bash
docker-compose up --build
```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md) - System design and patterns
- [API Documentation](docs/api.md) - REST API endpoints
- [Developer Guide](docs/developer-guide.md) - Development workflow

## 🔐 Security

- JWT-based authentication
- Role-based access control (RBAC)
- Secure password hashing
- API rate limiting
- SQL injection prevention
- XSS protection

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
python manage.py test
```

## 📦 Deployment

The system is containerized and production-ready. See [deployment guide](docs/deployment.md) for details.

## 🤝 Development Workflow

1. Each module is self-contained with clear boundaries
2. API contracts are documented in `docs/api.md`
3. Database schema is versioned in `database/schema.md`
4. Follow the established patterns in existing modules
5. Every feature has corresponding tests

## 📄 License

Proprietary - All rights reserved

## 👥 Support

For questions and support, refer to the documentation or contact the development team.
