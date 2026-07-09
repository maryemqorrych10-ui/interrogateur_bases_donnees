# 🗄️ Interrogateur de Bases de Données

Une application web complète pour interroger et gérer n'importe quelle base de données avec une interface moderne et réactive.

## ✨ Fonctionnalités

✅ **Multi-Base de Données**
- PostgreSQL, MySQL, SQLite, MongoDB
- Gestion illimitée de connexions
- Sauvegarde des connexions

✅ **Éditeur de Requêtes**
- Interface intuitive pour écrire des requêtes
- Exécution en temps réel
- Affichage des résultats en tableau

✅ **Export de Données**
- Export en JSON
- Export en CSV
- Téléchargement direct

✅ **Historique des Requêtes**
- Enregistrement automatique
- Temps d'exécution
- Gestion des erreurs

✅ **Interface Moderne**
- Design responsive (mobile, tablet, desktop)
- Gradients élégants
- Navigation intuitive

## 🏗️ Architecture

```
interrogateur_bases_donnees/
├── backend/              # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── main.py       # Application principale
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Connecteur BD
│   │   ├── models.py     # Modèles SQLAlchemy
│   │   ├── schemas.py    # Schémas Pydantic
│   │   └── routers/
│   │       ├── connections.py  # API Connexions
│   │       └── queries.py      # API Requêtes
│   ├── requirements.txt
│   └── .env
├── frontend/             # React + Vite
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Connections.jsx
│   │   │   ├── QueryEditor.jsx
│   │   │   └── QueryHistory.jsx
│   │   └── styles/
│   │       ├── Connections.css
│   │       ├── QueryEditor.css
│   │       └── QueryHistory.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.9+
- Node.js 16+
- npm ou yarn

### Backend (FastAPI)

1. **Installer les dépendances**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configurer l'environnement**
   ```bash
   cp .env.example .env
   # Modifier .env si nécessaire
   ```

3. **Lancer le serveur**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   Le backend sera disponible à: **http://localhost:8000**
   
   Documentation API Swagger: **http://localhost:8000/docs**

### Frontend (React)

1. **Installer les dépendances**
   ```bash
   cd frontend
   npm install
   ```

2. **Lancer le serveur de développement**
   ```bash
   npm run dev
   ```
   Le frontend sera disponible à: **http://localhost:5173**

3. **Build pour la production**
   ```bash
   npm run build
   ```

## 📡 API Endpoints

### Connexions

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/connections` | Créer une connexion |
| GET | `/api/connections` | Lister les connexions |
| GET | `/api/connections/{id}` | Obtenir une connexion |
| PUT | `/api/connections/{id}` | Mettre à jour une connexion |
| DELETE | `/api/connections/{id}` | Supprimer une connexion |
| POST | `/api/connections/{id}/test` | Tester une connexion |

### Requêtes

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/queries/execute` | Exécuter une requête |
| GET | `/api/queries/history` | Obtenir l'historique |
| DELETE | `/api/queries/history/{id}` | Supprimer une entrée |
| POST | `/api/queries/export` | Exporter les résultats |

## 🔧 Configuration

### Variables d'environnement (.env)

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here-change-in-production
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=True
```

## 📝 Exemples d'Utilisation

### 1. Ajouter une connexion PostgreSQL

```bash
curl -X POST http://localhost:8000/api/connections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ma BD Postgres",
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "database": "mydb"
  }'
```

### 2. Exécuter une requête

```bash
curl -X POST http://localhost:8000/api/queries/execute \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": 1,
    "query": "SELECT * FROM users LIMIT 10"
  }'
```

### 3. Exporter les résultats

```bash
curl -X POST http://localhost:8000/api/queries/export \
  -H "Content-Type: application/json" \
  -d '{
    "format": "csv",
    "data": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    "filename": "results"
  }'
```

## 🎨 Interface Utilisateur

### Pages Principales

1. **Connexions** 🔗
   - Liste des connexions configurées
   - Ajouter une nouvelle connexion
   - Tester les connexions
   - Supprimer les connexions

2. **Éditeur de Requêtes** 📝
   - Interface pour écrire des requêtes
   - Sélection de la base de données
   - Exécution et visualisation des résultats
   - Export en JSON/CSV

3. **Historique** 📋
   - Historique complet des requêtes exécutées
   - Statut de chaque requête
   - Temps d'exécution
   - Messages d'erreur

## 🛠️ Technologies

### Backend
- **FastAPI** - Framework web async
- **SQLAlchemy** - ORM pour les bases de données
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI
- **python-dotenv** - Gestion des variables d'environnement

### Frontend
- **React 18** - Framework UI
- **Vite** - Build tool rapide
- **Axios** - Client HTTP
- **React Router** - Routage
- **Tailwind CSS** - Styles
- **React Icons** - Icônes

## 📦 Dépendances

### Backend
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
psycopg2-binary==2.9.9
pymysql==1.1.0
pymongo==4.6.0
```

### Frontend
```
react: ^18.2.0
react-dom: ^18.2.0
axios: ^1.6.0
react-router-dom: ^6.20.0
vite: ^5.0.8
```

## 🚨 Gestion des Erreurs

L'application gère gracieusement les erreurs:

- **Erreurs de connexion** - Messages clairs et testeur de connexion
- **Erreurs de requête** - Affichage détaillé des erreurs SQL
- **Erreurs d'export** - Validation avant export
- **Timeouts** - Gestion des requêtes longues

## 🔒 Sécurité

- ✅ CORS configuré
- ✅ Validation Pydantic
- ✅ Pas de stockage de mots de passe en clair (à améliorer)
- ✅ SQL basé sur ORM (prévention SQL injection)

### À Améliorer
- [ ] Authentification utilisateur
- [ ] Chiffrement des mots de passe
- [ ] Rate limiting
- [ ] Logs d'audit
- [ ] HTTPS en production

## 📊 Performances

- Temps d'exécution des requêtes affichés
- Pagination pour les grands ensembles de données
- Gestion des requêtes asynchrones
- Cache des connexions

## 🤝 Contribution

Les contributions sont bienvenues! Veuillez:

1. Fork le repository
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

MIT License - Voir le fichier LICENSE

## 📧 Support

Pour les questions ou problèmes, veuillez ouvrir une issue sur GitHub.

## 🎯 Roadmap

- [ ] Authentification utilisateur
- [ ] Stockage sécurisé des mots de passe
- [ ] Requêtes sauvegardées et favoris
- [ ] Collaboration en temps réel
- [ ] Dashboard avec statistiques
- [ ] Support de plus de bases de données
- [ ] Visualisation graphique des résultats
- [ ] Import de données
- [ ] Schéma visualizer
- [ ] Dark mode

---

**Développé avec ❤️ par l'équipe**
