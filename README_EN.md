# 🔐 EGAuth - Centralized Authentication System (OpenID Connect)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.128-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue)
![License](https://img.shields.io/badge/license-MIT-green)

🇬🇧 English | 🇫🇷 [Version Française](README.md)

**EGAuth** is a centralized authentication server fully compliant with **OpenID Connect (OIDC)** and **OAuth 2.0** standards. It enables multiple SaaS applications (EGSaas1, EGSaas2, etc.) to share a unified authentication system.

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Getting Started](#-getting-started)
- [Web Interfaces](#-web-interfaces)
- [REST API](#-rest-api)
- [Architecture](#-architecture)
- [OIDC Workflows](#-oidc-workflows)
- [Production Deployment](#-production-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Authentication

✅ **Secure user registration** with Argon2 hashing  
✅ **Login** with email and password  
✅ **JWT tokens** signed with RSA-256  
✅ **Refresh tokens** for extended sessions  
✅ **Token revocation** management  

### OAuth 2.0 & OpenID Connect

✅ **Authorization Code Flow** (recommended)  
✅ **PKCE support** for enhanced security  
✅ **ID Tokens** OIDC-compliant  
✅ **Access Tokens** for API access  
✅ **Scopes**: openid, profile, email, offline_access  

### OIDC Discovery

✅ **`.well-known/openid-configuration` endpoint**  
✅ **`.well-known/jwks.json` endpoint** for token validation  
✅ **Auto-discovery** by clients  

### Multi-SaaS Management

✅ **Multiple OAuth clients**  
✅ **Configurable redirect URIs**  
✅ **Custom scopes** per client  
✅ **Secure client secrets**  

### Modern Web Interfaces

✅ **User registration form**  
✅ **OAuth client registration form**  
✅ **Login page**  
✅ **Responsive design**  
✅ **Professional theme** with cohesive colors  

---

## 📦 Requirements

- **Python** 3.12+
- **PostgreSQL** 14+
- **Docker** & **Docker Compose** (optional)
- **Git**

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/epiphane-gedeon/EGAuth.git
cd EGAuth
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

**Option A: Using Docker Compose**

```bash
docker compose up -d
```

**Option B: Local PostgreSQL**

Make sure PostgreSQL is installed and running locally.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/egauth

# Tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# RSA Keys
PRIVATE_KEY_PATH=keys/private.pem
PUBLIC_KEY_PATH=keys/public.pem
```

### 6. Generate RSA keys

```bash
python -c 'from app.security.rsa_keys import load_or_create_keys; load_or_create_keys("keys/private.pem", "keys/public.pem"); print("✅ Keys generated")'
```

### 7. Initialize the database

```bash
python verify_app.py --create
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | str | - | PostgreSQL connection URL |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | 30 | Access token expiration time |
| `REFRESH_TOKEN_EXPIRE_DAYS` | int | 30 | Refresh token expiration time |
| `PRIVATE_KEY_PATH` | str | `keys/private.pem` | Path to RSA private key |
| `PUBLIC_KEY_PATH` | str | `keys/public.pem` | Path to RSA public key |

---

## 🎬 Getting Started

### Development mode

```bash
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at **http://localhost:8000**

### API Documentation

```
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)
```

### Verify database

```bash
python verify_app.py
```

This script verifies:
- PostgreSQL connection ✅
- All tables present ✅
- SQLAlchemy models validity ✅
- Pydantic schemas validity ✅
- Record counts ✅

---

## 🎨 Web Interfaces

### 1. User Registration

**URL**: `http://localhost:8000/users/register-form`

**Modern HTML form with:**
- Email (required, validation)
- Username (required)
- Password (required)
- First name (optional)
- Last name (optional)

**POST** (`/users/register`):
```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. OAuth Client Registration

**URL**: `http://localhost:8000/clients/register-form`

**Form to create an OAuth application:**
- Application name (required)
- Redirect URIs (required, one per line)
- Requested scopes (checkboxes: openid, profile, email, offline_access)

**POST** (`/clients/register`):
```json
{
  "name": "My Amazing App",
  "redirect_uris": [
    "http://localhost:3000/callback",
    "https://myapp.com/auth/callback"
  ],
  "allowed_scopes": ["openid", "profile", "email"]
}
```

**Response**:
```json
{
  "client_id": "egauth_xxxxx",
  "client_secret": "xxxxxxxxxxxx",
  "name": "My Amazing App",
  "redirect_uris": [...],
  "allowed_scopes": [...]
}
```

### 3. Login Page

**URL**: `http://localhost:8000/authorize`

OAuth2/OIDC login page for users.

---

## 🔧 REST API

### Authentication

#### POST `/auth/login`
User login
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### POST `/users/register`
Register a new user

#### GET `/users/me`
Get authenticated user (requires Bearer token)

#### POST `/auth/refresh`
Refresh the access token

### OAuth 2.0 / OIDC

#### GET `/authorize`
Initiate authorization flow

```
GET /authorize?
  client_id=egauth_xxxxx&
  redirect_uri=http://localhost:3000/callback&
  response_type=code&
  scope=openid%20profile%20email&
  state=random_state
```

#### POST `/token`
Exchange authorization code for tokens

```json
{
  "code": "authorization_code",
  "client_id": "egauth_xxxxx",
  "client_secret": "secret",
  "redirect_uri": "http://localhost:3000/callback"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "id_token": "eyJhbGc...",
  "token_type": "Bearer"
}
```

#### GET `/userinfo`
Get user information (Bearer token required)

#### GET `/.well-known/openid-configuration`
OIDC discovery endpoint

#### GET `/.well-known/jwks.json`
Public keys for JWT validation

---

## 🏗️ Architecture

```
EGAuth/
├── app/
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── config.py              # Configuration
│   ├── database.py            # Database connection
│   ├── main.py                # FastAPI application
│   ├── routes/                # API endpoints
│   │   ├── auth.py            # Authentication
│   │   ├── users.py           # User management
│   │   ├── clients.py         # OAuth client management
│   │   └── oidc.py            # OIDC discovery
│   ├── services/              # Business logic
│   │   ├── user_service.py
│   │   ├── client_service.py
│   │   └── token_service.py
│   ├── security/              # Security
│   │   ├── rsa_keys.py        # RSA key management
│   │   └── jwt_handler.py     # JWT handling
│   ├── template/              # HTML templates
│   ├── static/                # CSS, images
│   └── __init__.py
├── alembic/                   # Database migrations
├── keys/                      # RSA keys (generated)
├── .env                       # Environment variables
├── docker-compose.yml         # Docker configuration
├── requirements.txt           # Python dependencies
├── verify_app.py              # Verification script
└── README.md                  # Documentation
```

---

## 🔐 OIDC Workflows

### 1. New User Registration

```
User
  ↓
Form /users/register-form
  ↓
POST /users/register
  ↓
Argon2 password hashing
  ↓
Database creation
  ↓
User created ✅
```

### 2. OAuth 2.0 Authentication Flow (Authorization Code)

```
User → Clicks "Sign in with EGAuth"
  ↓
Redirected to /authorize
  ↓
User enters email/password
  ↓
Authorization code created (10 min valid)
  ↓
Redirect with code to client
  ↓
Client exchanges code for tokens (POST /token)
  ↓
Access Token, Refresh Token, ID Token returned
  ↓
Client can fetch user info (/userinfo)
```

### 3. Token Refresh

```
Client detects token expiration
  ↓
Sends refresh_token to POST /token
  ↓
Refresh token verification
  ↓
New access_token generated
  ↓
Resource access restored ✅
```

---

## 🌐 Production Deployment

### 1. Secure configuration

```env
# Use HTTPS mandatory
DATABASE_URL=postgresql+asyncpg://user:password@prod-server:5432/egauth

# Keys stored securely (AWS Secrets Manager, HashiCorp Vault, etc.)
PRIVATE_KEY_PATH=/etc/egauth/private.pem
PUBLIC_KEY_PATH=/etc/egauth/public.pem

# Shorter token lifetimes
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 2. Docker deployment

```bash
docker compose -f docker-compose.yml up -d
```

### 3. Nginx/Apache configuration

Configure a reverse proxy with SSL/TLS in front of the application.

### 4. SSL/TLS

Mandatory in production. Use Let's Encrypt or a signed certificate.

### 5. Database

- Regular backups
- Replication for high availability
- Performance monitoring

### 6. Monitoring

- Centralized logging (ELK, Splunk)
- Alerting (errors, timeouts)
- Metrics (Prometheus, Grafana)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is under MIT license. See the `LICENSE` file for details.

---

## 📞 Support

For questions or issues, please open an [issue](https://github.com/epiphane-gedeon/EGAuth/issues).

---

**Made with ❤️ by Epiphane Gedeon**
