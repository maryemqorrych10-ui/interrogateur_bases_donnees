# Scripts de démarrage rapide

## Lancer l'application complète

### Avec Docker Compose (recommandé)
```bash
docker-compose up
```

Puis visitez:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentation Swagger: http://localhost:8000/docs

### Sans Docker

#### 1. Démarrer le backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### 2. Dans un nouveau terminal, démarrer le frontend
```bash
cd frontend
npm install
npm run dev
```

## Structure des Fichiers

```
interrogateur_bases_donnees/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # Application principale
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Connexions BD
│   │   ├── models.py       # Modèles
│   │   ├── schemas.py      # Schémas
│   │   └── routers/
│   │       ├── connections.py
│   │       └── queries.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env
│   └── .gitignore
├── frontend/               # Application React
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── index.css
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
│   ├── index.html
│   ├── Dockerfile
│   ├── .env.local
│   └── .gitignore
├── docker-compose.yml
├── README.md
└── QUICKSTART.md
```

## API Endpoints Rapides

### Créer une Connexion
```bash
curl -X POST http://localhost:8000/api/connections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ma BD",
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "database": "mydb"
  }'
```

### Exécuter une Requête
```bash
curl -X POST http://localhost:8000/api/queries/execute \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": 1,
    "query": "SELECT * FROM users LIMIT 5"
  }'
```

### Lister les Connexions
```bash
curl http://localhost:8000/api/connections
```

### Historique des Requêtes
```bash
curl http://localhost:8000/api/queries/history
```

## Troubleshooting

### Problème: Port 8000 déjà utilisé
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problème: Erreur de connexion BD
- Vérifier les identifiants
- Vérifier que la BD est running
- Vérifier les pare-feu
- Utiliser le bouton "Tester" pour diagnostiquer

### Problème: Frontend ne voit pas le backend
- Vérifier que le backend est running sur le port 8000
- Vérifier les CORS dans .env du backend
- Ouvrir la console du navigateur (F12) pour voir les erreurs

## Contrôles de Sécurité Avant Production

- [ ] Changer SECRET_KEY dans .env
- [ ] Désactiver DEBUG=False en production
- [ ] Configurer HTTPS
- [ ] Ajouter authentification utilisateur
- [ ] Chiffrer les mots de passe BD
- [ ] Mettre en place rate limiting
- [ ] Configurer logs d'audit
- [ ] Tester les vulnérabilités SQL

## Performance

- Temps d'exécution mesuré pour chaque requête
- Historique stocké en BD pour analyse
- Résultats limités pour éviter surcharge mémoire

## Support

Pour les problèmes:
1. Vérifier la console du navigateur (F12)
2. Vérifier les logs du backend
3. Ouvrir une issue sur GitHub

---

**Bonne utilisation! 🚀**
