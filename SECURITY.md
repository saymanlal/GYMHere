# Security Best Practices

## 🔐 GitGuardian Alert - False Positives Explained

If you're seeing GitGuardian alerts on this repository, they're likely **false positives** from example/template files. Here's why:

### Files That Contain Example Credentials

1. **`backend/.env.example`** - Template file showing required environment variables
2. **`backend/README.md`** - Documentation showing configuration examples
3. **`docs/developer-guide.md`** - Setup guide with example values

**These are NOT real credentials.** They are placeholders meant to guide developers.

### How to Handle GitGuardian Alerts

#### For `.env.example` Files
These files should NEVER contain real secrets. They exist to show:
- What environment variables are needed
- The format/structure of the values
- Example placeholder values

**Action**: Mark as "False Positive" in GitGuardian

#### For README/Documentation Files
Documentation may include example configurations that look like secrets but are clearly marked as examples.

**Action**: Mark as "False Positive" in GitGuardian

---

## 🛡️ Real Security Practices

### 1. Environment Variables

**NEVER commit actual `.env` files!**

```bash
# ✅ Good - In .gitignore
.env
.env.local
.env.production

# ✅ Good - Template file
.env.example
```

**Always use strong, unique values in production:**

```bash
# ❌ Bad
SECRET_KEY=django-insecure-dev-key
DB_PASSWORD=postgres

# ✅ Good
SECRET_KEY=<50+ character random string>
DB_PASSWORD=<complex unique password>
```

### 2. Generate Secure Secret Keys

**Django Secret Key:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**Or use:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Database Credentials

**Development:**
```env
DB_PASSWORD=dev_password_123  # Only for local development
```

**Production:**
```env
DB_PASSWORD=<use password manager or secrets vault>
```

**Best Practice**: Use managed database services (AWS RDS, Azure Database, etc.) with IAM authentication when possible.

### 4. API Keys & Tokens

**NEVER hardcode API keys:**

```python
# ❌ Bad
api_key = "sk_live_abc123xyz789"

# ✅ Good
import os
api_key = os.environ.get('API_KEY')
```

### 5. Email Credentials

**Gmail App Passwords:**
1. Enable 2FA on your Google account
2. Generate an App Password (not your regular password)
3. Store in environment variables
4. Use different credentials for dev/staging/production

```env
# Development
EMAIL_HOST_USER=dev@example.com
EMAIL_HOST_PASSWORD=<dev app password>

# Production  
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=<production app password>
```

### 6. JWT Secret Keys

**Generate strong JWT secrets:**

```python
import secrets
print(secrets.token_urlsafe(50))
```

**Configure different secrets per environment:**

```env
# Never use the same secret across environments!
# Development
JWT_SECRET=dev_secret_xyz

# Production
JWT_SECRET=<50+ character unique secret>
```

---

## 🔒 What to NEVER Commit

- ❌ `.env` files with real credentials
- ❌ API keys or tokens
- ❌ Database passwords
- ❌ JWT secret keys
- ❌ AWS/Azure/GCP credentials
- ❌ Private SSH keys
- ❌ OAuth client secrets
- ❌ Encryption keys

## ✅ What's Safe to Commit

- ✅ `.env.example` with placeholder values
- ✅ Documentation with example credentials
- ✅ Configuration templates
- ✅ Code that reads from environment variables

---

## 🚨 If You Accidentally Commit Secrets

1. **Rotate the Secret Immediately**
   - Change the password/key/token
   - Revoke the old one

2. **Remove from Git History**
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   # This is complex - see GitHub docs
   ```

3. **Force Push** (if not on main/master)
   ```bash
   git push --force
   ```

4. **Notify Team** if it's a shared repository

---

## 🔐 Production Deployment Security

### Environment Variables Management

**Option 1: Cloud Provider Secrets**
- AWS: Secrets Manager, Systems Manager Parameter Store
- Azure: Key Vault
- GCP: Secret Manager
- Heroku: Config Vars

**Option 2: Docker Secrets**
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env.production  # Not committed to git
```

**Option 3: Kubernetes Secrets**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gym-secrets
type: Opaque
data:
  secret-key: <base64 encoded>
```

### Django Production Settings

```python
# settings/production.py

# ✅ Required security settings
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# ✅ HTTPS enforcement
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ✅ Security headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## 📋 Security Checklist

**Before First Deploy:**
- [ ] All `.env` files in `.gitignore`
- [ ] Strong SECRET_KEY generated
- [ ] Unique database password
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Database backups configured

**Regular Maintenance:**
- [ ] Rotate secrets quarterly
- [ ] Update dependencies monthly
- [ ] Review access logs
- [ ] Monitor for security alerts
- [ ] Keep Django/packages updated

---

## 🔍 Tools for Security

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

### Secret Scanning
- **GitGuardian** - Automated secret detection (already setup)
- **git-secrets** - Prevent commits with secrets
- **truffleHog** - Find secrets in git history

### Dependency Scanning
```bash
# Python
pip install safety
safety check

# Node.js
npm audit
```

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Docs](https://docs.djangoproject.com/en/stable/topics/security/)
- [12-Factor App](https://12factor.net/)
- [GitGuardian Best Practices](https://www.gitguardian.com/secrets-detection)

---

## ⚠️ Important Note

**This project's example files are intentionally marked with placeholder values.**

Any credentials in:
- `*.example` files
- Documentation files
- README files

Are **NOT real secrets** and are safe to commit. They serve as templates for developers to create their own configuration files.

Real credentials should ONLY exist in:
- Your local `.env` file (gitignored)
- Your production secrets manager
- Environment variables on your deployment platform

**Never share or commit real credentials!**