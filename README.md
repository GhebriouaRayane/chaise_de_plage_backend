# Beach Chair Shop Backend - FastAPI

Ce projet est le backend complet pour le site de vente de chaises de plage, conçu pour être déployé sur **Render** avec une base de données **Supabase (PostgreSQL)**.

## Fonctionnalités

- **Gestion des Produits & Catégories** : CRUD complet.
- **Gestion des Commandes** : Calcul automatique des frais de livraison pour les 58 wilayas d'Algérie.
- **Livraison Gratuite** : Automatique à partir de 2 chaises.
- **Notifications Email** : Envoi automatique à l'admin et confirmation au client.
- **Interface Admin** : Sécurisée via JWT pour gérer les commandes et changer leur statut.
- **Sécurité** : Mots de passe chiffrés avec bcrypt et authentification JWT.

## Structure du Projet

```text
app/
├── api/v1/endpoints/  # Routes API (auth, products, orders, contact)
├── core/              # Configuration et Sécurité
├── crud/              # Logique d'accès aux données
├── db/                # Session SQLAlchemy
├── models/            # Modèles de base de données
├── schemas/           # Schémas Pydantic (validation)
├── services/          # Logique métier (Wilayas, Emails)
└── templates/         # Interface Admin HTML
main.py                # Point d'entrée de l'application
init_db.py             # Script d'initialisation de la base
```

## Déploiement

### 1. Base de données (Supabase)
1. Créez un projet sur [Supabase](https://supabase.com/).
2. Copiez la **Connection String** (Transaction mode) dans les paramètres de la base de données.

### 2. Déploiement sur Render
1. Créez un nouveau **Web Service** sur [Render](https://render.com/).
2. Connectez votre dépôt GitHub.
3. Configurez les variables d'environnement (voir `.env.example`).
4. La commande de build est `pip install -r requirements.txt`.
5. La commande de démarrage est `uvicorn main:app --host 0.0.0.0 --port $PORT`.

### 3. Initialisation
Une fois déployé, exécutez le script d'initialisation pour créer les tables et les produits par défaut :
```bash
python init_db.py
```

## Variables d'Environnement (.env)

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | URL de connexion PostgreSQL (Supabase) |
| `SECRET_KEY` | Clé secrète pour JWT |
| `ADMIN_USERNAME` | Nom d'utilisateur admin |
| `ADMIN_PASSWORD` | Mot de passe admin |
| `SMTP_HOST` | Serveur SMTP (ex: smtp.gmail.com) |
| `SMTP_USER` | Email pour l'envoi |
| `SMTP_PASSWORD` | Mot de passe d'application SMTP |
| `BACKEND_CORS_ORIGINS` | URL de votre frontend sur Cloudflare Pages |

## Documentation API
Accédez à `/docs` pour la documentation Swagger interactive.
Accédez à `/admin` pour l'interface de gestion des commandes.
