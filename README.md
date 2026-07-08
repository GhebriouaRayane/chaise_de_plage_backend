# Beach Chair Shop Backend - FastAPI

Ce projet est le backend complet pour le site de vente de chaises de plage.
Il peut tourner en local avec une base **SQLite** par défaut, puis etre adapte plus tard a **PostgreSQL/Supabase** pour la production.

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

## Lancement en local

### 1. Aller dans le dossier backend
```bash
cd "backend de site vitrine chaises"
```

### 2. Créer l'environnement Python
Si le venv existe deja, active-le. Sinon, cree-en un nouveau.

```bash
python -m venv .venv
source .venv/bin/activate
```

Sur Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Installer les dependances
```bash
pip install -r requirements.txt
```

### 4. Preparer la base locale
Le fichier `.env` est deja configure pour SQLite:
```env
DATABASE_URL=sqlite:///./beach_chair.db
```

Puis initialise les tables et les produits de demo:
```bash
python init_db.py
```

### 5. Lancer le backend
```bash
uvicorn main:app --reload
```

Le backend sera accessible sur:
```text
http://127.0.0.1:8000
```

La documentation Swagger est ici:
```text
http://127.0.0.1:8000/docs
```

## Lancement du frontend

Dans un autre terminal:
```bash
cd "frontend de site vitrine chaises"
npm install
npm run dev
```

Le frontend sera accessible sur:
```text
http://localhost:5173
```

## Déploiement

### 1. Base de données (Supabase)
1. Créez un projet sur [Supabase](https://supabase.com/).
2. Copiez la connection string dans les variables d'environnement.

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
| `DATABASE_URL` | URL de connexion base de donnees, par exemple `sqlite:///./beach_chair.db` en local |
| `SECRET_KEY` | Clé secrète pour JWT |
| `ADMIN_USERNAME` | Nom d'utilisateur admin |
| `ADMIN_PASSWORD` | Mot de passe admin |
| `SMTP_HOST` | Serveur SMTP si tu veux activer les emails |
| `SMTP_USER` | Email pour l'envoi |
| `SMTP_PASSWORD` | Mot de passe d'application SMTP |
| `FRONTEND_URL` | URL du frontend, par exemple `http://localhost:5173` |
| `BACKEND_CORS_ORIGINS` | Origines autorisees pour le frontend local |

## Documentation API
Accédez à `/docs` pour la documentation Swagger interactive.
Accédez à `/admin` pour l'interface de gestion des commandes.
