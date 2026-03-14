# API Documentation

## Base URL
```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Auth Endpoints

#### POST /auth/register/
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone": "+1234567890",
      "role": null,
      "is_active": true,
      "is_verified": false,
      "full_name": "John Doe",
      "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
      "access": "eyJ...",
      "refresh": "eyJ..."
    }
  },
  "message": "Registration successful"
}
```

#### POST /auth/login/
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "tokens": {
      "access": "eyJ...",
      "refresh": "eyJ..."
    }
  },
  "message": "Login successful"
}
```

#### POST /auth/logout/
Logout and blacklist refresh token.

**Request:**
```json
{
  "refresh": "eyJ..."
}
```

#### GET /auth/me/
Get current user details.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    ...
  }
}
```

#### PATCH /auth/me/update/
Update user profile.

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

#### POST /auth/change-password/
Change password.

**Request:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewPass123!"
}
```

#### POST /auth/refresh/
Refresh access token.

**Request:**
```json
{
  "refresh": "eyJ..."
}
```

**Response:**
```json
{
  "access": "eyJ..."
}
```

## Members

### Member Endpoints

#### GET /members/
Get paginated list of members.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `page_size` (integer, optional): Items per page (default: 20)
- `status` (string, optional): Filter by status (active, inactive, suspended, expired)
- `search` (string, optional): Search by name, email, phone, member code
- `ordering` (string, optional): Sort field (e.g., "-created_at", "first_name")

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "member_code": "GYM001",
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "status": "active",
      "joined_date": "2024-01-01",
      "has_active_subscription": true
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

#### GET /members/{id}/
Get single member details.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "member_code": "GYM001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+1234567891",
    "blood_group": "O+",
    "medical_conditions": "None",
    "profile_photo": "http://...",
    "status": "active",
    "joined_date": "2024-01-01",
    "notes": "VIP member",
    "full_name": "John Doe",
    "age": 34,
    "has_active_subscription": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### POST /members/
Create new member.

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01",
  "gender": "male",
  "address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567891",
  "blood_group": "O+",
  "medical_conditions": "None",
  "notes": "VIP member"
}
```

**Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Member created successfully"
}
```

#### PATCH /members/{id}/
Update member.

**Request:**
```json
{
  "first_name": "John",
  "phone": "+1234567890",
  "status": "active"
}
```

#### DELETE /members/{id}/
Delete member.

**Response:**
```json
{
  "success": true,
  "message": "Member deleted successfully"
}
```

#### POST /members/{id}/activate/
Activate member.

#### POST /members/{id}/deactivate/
Deactivate member.

#### POST /members/{id}/suspend/
Suspend member.

#### GET /members/stats/
Get member statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 150,
    "active": 120,
    "inactive": 20,
    "suspended": 5,
    "expired": 5
  }
}
```

#### GET /members/search/?q={query}
Search members by name, email, phone, or member code.

**Response:**
```json
{
  "success": true,
  "data": [...]
}
```

### Lead Endpoints

#### GET /members/leads/
Get paginated list of leads.

**Query Parameters:**
- `page`, `page_size`, `search`, `ordering` (same as members)
- `status` (string, optional): Filter by status (new, contacted, interested, converted, lost)
- `source` (string, optional): Filter by source

#### GET /members/leads/{id}/
Get single lead details.

#### POST /members/leads/
Create new lead.

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "source": "walk_in",
  "interested_plan": "uuid",
  "assigned_to": "uuid",
  "follow_up_date": "2024-01-15",
  "notes": "Interested in premium plan"
}
```

#### PATCH /members/leads/{id}/
Update lead.

#### POST /members/leads/{id}/convert/
Convert lead to member.

**Request:**
```json
{
  "member_data": {
    "date_of_birth": "1990-01-01",
    "gender": "male",
    ...
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": { ... },  // Created member data
  "message": "Lead converted to member successfully"
}
```

#### GET /members/leads/stats/
Get lead statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 50,
    "new": 15,
    "contacted": 10,
    "interested": 8,
    "converted": 12,
    "lost": 5,
    "conversion_rate": 24.0
  }
}
```

## Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field_name": ["Error message for this field"]
    }
  }
}
```

### Common Error Codes

- `VALIDATION_ERROR`: Invalid input data
- `INVALID_CREDENTIALS`: Wrong email or password
- `ACCOUNT_DISABLED`: User account is disabled
- `PERMISSION_DENIED`: User doesn't have required permission
- `NOT_FOUND`: Resource not found
- `ALREADY_EXISTS`: Resource already exists

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

## Pagination

List endpoints return paginated results:

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## Filtering & Searching

Most list endpoints support:
- **Filtering**: `?status=active&gender=male`
- **Searching**: `?search=john`
- **Ordering**: `?ordering=-created_at` (prefix with `-` for descending)

## Date Formats

All dates use ISO 8601 format:
- Dates: `YYYY-MM-DD` (e.g., `2024-01-01`)
- DateTimes: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2024-01-01T12:00:00Z`)