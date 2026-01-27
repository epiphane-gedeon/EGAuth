app/
│
├── main.py                # Point d’entrée FastAPI
│
├── core/                  # Config globale
│   ├── config.py
│   └── security.py
│
├── db/
│   ├── database.py        # Connexion DB
│   └── base.py            # Base ORM
│
├── models/                # Tables SQLAlchemy
│   ├── user.py
│   ├── link.py
│   ├── click.py
│   └── anonymous.py
│
├── schemas/               # Pydantic (entrées/sorties API)
│   ├── user.py
│   ├── link.py
│   └── stats.py
│
├── crud/                  # Logique DB pure
│   ├── user.py
│   ├── link.py
│   └── click.py
│
├── services/              # Logique métier
│   ├── link_service.py
│   └── analytics_service.py
│
├── api/
│   ├── deps.py            # dépendances FastAPI
│   ├── routes/
│   │   ├── auth.py
│   │   ├── links.py
│   │   └── stats.py
│
└── utils/
    ├── tokens.py
    ├── alias_generator.py
    └── rate_limiter.py
