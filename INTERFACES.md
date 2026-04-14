# 🎨 Interfaces Graphiques EGAuth

## Accès aux formulaires

### Enregistrement Utilisateur
- **URL** : http://localhost:8000/users/register-form
- **Formulaire** : Enregistrement de nouveaux utilisateurs
- **Champs** :
  - Email (obligatoire)
  - Nom d'utilisateur (obligatoire)
  - Mot de passe (obligatoire)
  - Prénom (optionnel)
  - Nom (optionnel)

### Enregistrement Client OAuth
- **URL** : http://localhost:8000/clients/register-form
- **Formulaire** : Enregistrement de nouvelles applications OAuth
- **Champs** :
  - Nom de l'application (obligatoire)
  - URIs de redirection (obligatoire, une par ligne)
  - Scopes demandés (checkboxes)
  - Résultat : Affichage du `client_id` et `client_secret`

## Intégration avec l'API

Les formulaires font des requêtes AJAX vers les endpoints API correspondants :

### Enregistrement Utilisateur
```bash
POST /users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Réponse** :
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Enregistrement Client
```bash
POST /clients/register
Content-Type: application/json

{
  "name": "Mon Application",
  "redirect_uris": ["http://localhost:3000/callback"],
  "allowed_scopes": ["openid", "profile", "email"]
}
```

**Réponse** :
```json
{
  "client_id": "egauth_xxxxxx",
  "client_secret": "xxxxxxxxxxxxx",
  "name": "Mon Application",
  "redirect_uris": ["http://localhost:3000/callback"],
  "allowed_scopes": ["openid", "profile", "email"]
}
```

## Fonctionnalités des Interfaces

✅ **Design moderne** avec gradient et animations
✅ **Validation en temps réel** côté client
✅ **Messages d'erreur** clairs et informatifs  
✅ **Chargement asynchrone** avec indicateur visuel
✅ **Copie des credentials** pour les clients OAuth
✅ **Responsive design** (mobile + desktop)
✅ **Accessibilité** (labels, aria, etc.)

## Lancer l'application

```bash
cd /home/epiphane-gedeon/EGAuth
source .venv/bin/activate

# Démarrer le serveur
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Tester dans le navigateur

1. **Créer un utilisateur** : http://localhost:8000/users/register-form
2. **Créer un client OAuth** : http://localhost:8000/clients/register-form
3. **Documentation API** : http://localhost:8000/docs
4. **Configuration OIDC** : http://localhost:8000/.well-known/openid-configuration
5. **Clés publiques** : http://localhost:8000/.well-known/jwks.json
