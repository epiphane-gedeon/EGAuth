# 🔐 EGAuth - Système d'Authentification Centralisé OpenID Connect

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.128-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**EGAuth** est un serveur d'authentification centralisé conforme aux normes **OpenID Connect (OIDC)** et **OAuth 2.0**. Il permet à plusieurs applications SaaS (EGSaas1, EGSaas2, etc.) de partager un système d'authentification unique.

## 📋 Table des matières

- [Caractéristiques](#-caractéristiques)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement](#-lancement)
- [Interfaces Graphiques](#-interfaces-graphiques)
- [API REST](#-api-rest)
- [Architecture](#-architecture)
- [Workflows OIDC](#-workflows-oidc)
- [Déploiement en Production](#-déploiement-en-production)
- [Contribution](#-contribution)
- [License](#-license)

---

## ✨ Caractéristiques

### Authentification
✅ **Enregistrement utilisateur** sécurisé avec hashage Argon2  
✅ **Connexion** avec email et mot de passe  
✅ **Tokens JWT** signés avec RSA-256  
✅ **Refresh tokens** pour les sessions longues  
✅ **Gestion de la révocation** des tokens  

### OAuth 2.0 & OpenID Connect
✅ **Authorization Code Flow** (recommandé)  
✅ **PKCE support** pour la sécurité  
✅ **ID Tokens** conformes OIDC  
✅ **Access Tokens** pour l'accès aux APIs  
✅ **Scopes** : openid, profile, email, offline_access  

### Discovery OIDC
✅ **Endpoint `.well-known/openid-configuration`**  
✅ **Endpoint `.well-known/jwks.json`** pour la validation des tokens  
✅ **Auto-découverte** par les clients  

### Gestion Multi-SaaS
✅ **Clients OAuth** multiples  
✅ **URIs de redirection** configurables  
✅ **Scopes personnalisés** par client  
✅ **Secrets clients** sécurisés  

### Interfaces Graphiques Modernes
✅ **Formulaire d'enregistrement utilisateur**  
✅ **Formulaire d'enregistrement client OAuth**  
✅ **Page de connexion**  
✅ **Design responsive** et cohérent  
✅ **Thème moderne** avec couleurs professionnelles  

---

## 📦 Prérequis

- **Python** 3.12+
- **PostgreSQL** 14+
- **Docker** & **Docker Compose** (optionnel)
- **Git**

---

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/epiphane-gedeon/EGAuth.git
cd EGAuth
```

### 2. Créer et activer l'environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Démarrer PostgreSQL

**Option A : Avec Docker Compose**

```bash
docker compose up -d
```

**Option B : PostgreSQL local**

Assure-toi que PostgreSQL est installé et démarré.

### 5. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet :

```env
# Base de données
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/egauth

# Tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Clés RSA
PRIVATE_KEY_PATH=keys/private.pem
PUBLIC_KEY_PATH=keys/public.pem
```

### 6. Générer les clés RSA

```bash
python -c 'from app.security.rsa_keys import load_or_create_keys; load_or_create_keys("keys/private.pem", "keys/public.pem"); print("✅ Clés générées")'
```

### 7. Initialiser la base de données

```bash
python verify_app.py --create
```

---

## ⚙️ Configuration

### Variables d'environnement (`.env`)

| Variable | Type | Défaut | Description |
|----------|------|--------|-------------|
| `DATABASE_URL` | str | - | URL de connexion PostgreSQL |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | 30 | Durée d'expiration du token d'accès |
| `REFRESH_TOKEN_EXPIRE_DAYS` | int | 30 | Durée d'expiration du token de rafraîchissement |
| `PRIVATE_KEY_PATH` | str | `keys/private.pem` | Chemin de la clé privée RSA |
| `PUBLIC_KEY_PATH` | str | `keys/public.pem` | Chemin de la clé publique RSA |

---

## 🎬 Lancement

### Mode développement

```bash
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

L'application sera disponible sur **http://localhost:8000**

### Documentation API

```
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)
```

### Vérifier la base de données

```bash
python verify_app.py
```

Ce script vérifie :
- Connexion à PostgreSQL ✅
- Présence de toutes les tables ✅
- Validité des modèles SQLAlchemy ✅
- Validité des schémas Pydantic ✅
- Nombre d'enregistrements ✅

---

## 🎨 Interfaces Graphiques

### 1. Enregistrement Utilisateur

**URL** : `http://localhost:8000/users/register-form`

**Formulaire HTML moderne avec :**
- Email (obligatoire, validation)
- Nom d'utilisateur (obligatoire)
- Mot de passe (obligatoire)
- Prénom (optionnel)
- Nom (optionnel)

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

### 2. Enregistrement Client OAuth

**URL** : `http://localhost:8000/clients/register-form`

**Formulaire pour créer une application OAuth :**
- Nom de l'application (obligatoire)
- URIs de redirection (obligatoire, une par ligne)
- Scopes demandés (checkboxes : openid, profile, email, offline_access)

**POST** (`/clients/register`):
```json
{
  "name": "Ma Superbe App",
  "redirect_uris": [
    "http://localhost:3000/callback",
    "https://monapp.com/auth/callback"
  ],
  "allowed_scopes": ["openid", "profile", "email"]
}
```

**Réponse** :
```json
{
  "client_id": "egauth_xxxxx",
  "client_secret": "xxxxxxxxxxxx",
  "name": "Ma Superbe App",
  "redirect_uris": [...],
  "allowed_scopes": [...]
}
```

### 3. Page de Connexion

**URL** : `http://localhost:8000/authorize`

Page de connexion OAuth2/OIDC pour les utilisateurs.

---

## 🔌 API REST

### Authentification

#### POST `/auth/login`
Connexion utilisateur
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### POST `/users/register`
Enregistrement utilisateur

#### GET `/users/me`
Récupérer l'utilisateur authentifié (requiert Bearer token)

#### POST `/auth/refresh`
Rafraîchir le token d'accès

### OAuth 2.0 / OIDC

#### GET `/authorize`
Initier le flux d'autorisation

```
GET /authorize?
  client_id=egauth_xxxxx&
  redirect_uri=http://localhost:3000/callback&
  response_type=code&
  scope=openid%20profile%20email&
  state=random_state
```

#### POST `/token`
Echanger un code d'autorisation pour des tokens

```json
{
  "code": "authorization_code",
  "client_id": "egauth_xxxxx",
  "client_secret": "secret",
  "redirect_uri": "http://localhost:3000/callback"
}
```

**Réponse** :
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "id_token": "eyJhbGc...",
  "token_type": "Bearer"
}
```

#### GET `/userinfo`
Récupérer les informations utilisateur (Bearer token)

#### GET `/.well-known/openid-configuration`
Découverte OIDC

#### GET `/.well-known/jwks.json`
Clés publiques pour validation JWT

---

## 🏗️ Architecture

```
EGAuth/
├── app/
│   ├── models.py              # Modèles SQLAlchemy
│   ├── schemas.py             # Schémas Pydantic
│   ├── config.py              # Configuration
│   ├── database.py            # Connexion BD
│   ├── main.py                # Application FastAPI
│   ├── routes/                # Endpoints API
│   │   ├── auth.py            # Authentification
│   │   ├── users.py           # Gestion utilisateurs
│   │   ├── clients.py         # Gestion clients OAuth
│   │   └── oidc.py            # Discovery OIDC
│   ├── services/              # Logique métier
│   │   ├── user_service.py
│   │   ├── client_service.py
│   │   └── token_service.py
│   ├── security/              # Sécurité
│   │   ├── rsa_keys.py        # Gestion clés RSA
│   │   └── jwt_handler.py     # JWT
│   ├── template/              # Templates HTML
│   ├── static/                # CSS, images
│   └── __init__.py
├── alembic/                   # Migrations BD
├── keys/                      # Clés RSA (généré)
├── .env                       # Variables d'environnement
├── docker-compose.yml         # Configuration Docker
├── requirements.txt           # Dépendances Python
├── verify_app.py              # Script de vérification
└── README.md                  # Ce fichier
```

---

## 🔐 Workflows OIDC

### 1. Enregistrement d'un nouvel utilisateur

```
Utilisateur
    ↓
Formulaire /users/register-form
    ↓
POST /users/register
    ↓
Hashage Argon2 du mot de passe
    ↓
Création en base de données
    ↓
Utilisateur créé ✅
```

### 2. Flux d'authentification OAuth 2.0 (Authorization Code)

```
Utilisateur → Clique "Se connecter avec EGAuth"
    ↓
Redirection vers /authorize
    ↓
Utilisateur entre email/password
    ↓
Création d'un code d'autorisation (10 min)
    ↓
Redirection avec code vers client
    ↓
Client échange code pour tokens (POST /token)
    ↓
Access Token, Refresh Token, ID Token retournés
    ↓
Client peut récupérer les infos utilisateur (/userinfo)
```

### 3. Rafraîchissement du token

```
Client détecte token expiré
    ↓
Envoie refresh_token à POST /token
    ↓
Vérification du refresh_token
    ↓
Génération d'un nouveau access_token
    ↓
Accès aux ressources rétabli ✅
```

---

## 🌐 Déploiement en Production

### 1. Configuration sécurisée

```env
# Utiliser HTTPS obligatoire
DATA_BASE_URL=postgresql+asyncpg://user:password@prod-server:5432/egauth

# Clés mises en place sécurisée (AWS Secrets Manager, HashiCorp Vault, etc.)
PRIVATE_KEY_PATH=/etc/egauth/private.pem
PUBLIC_KEY_PATH=/etc/egauth/public.pem

# Tokens plus courts
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 2. Déploiement avec Docker

```bash
docker compose -f docker-compose.yml up -d
```

### 3. Configuration Nginx/Apache

Configurer un reverse proxy SSL/TLS devant l'application.

### 4. SSL/TLS

Obligatoire en production. Utiliser Let's Encrypt ou un certificat signé.

### 5. Base de données

- Backups réguliers
- Réplication pour haute disponibilité
- Monitoring des performances

### 6. Monitoring

- Logs centralisés (ELK, Splunk)
- Alertes (alerting sur erreurs, timeouts)
- Métriques (Prometheus, Grafana)

---

## 🤝 Contribution

Les contributions sont bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

---

## 📄 License

Ce projet est sous license MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 📞 Support

Pour toute question ou problème, ouvrez une [issue](https://github.com/epiphane-gedeon/EGAuth/issues).

---

**Fait avec ❤️ par Epiphane-Gedeon**