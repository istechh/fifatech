# ISO Predict — Frontend

Interface de prédiction de matches internationaux, consommant l'API FastAPI du dossier [`../app`](../app). Stack : React 19 + TypeScript + Vite + Tailwind CSS v4, graphiques Recharts, tests Vitest/Testing Library, lint Oxlint.

## Démarrage local

```bash
npm install
cp .env.example .env.local   # ajuste VITE_API_URL si l'API ne tourne pas en local sur :8000
npm run dev
```

L'API backend doit tourner en parallèle (voir `../run.sh` ou `uvicorn app.api:app --reload` à la racine du repo).

## Scripts

| Commande | Rôle |
|---|---|
| `npm run dev` | Serveur de dev avec HMR |
| `npm run build` | Typecheck (`tsc -b`) + build de production dans `dist/` |
| `npm run preview` | Sert le build de production en local |
| `npm run lint` | Lint (Oxlint, avec le plugin `jsx-a11y` pour l'accessibilité) |
| `npm run format` / `format:check` | Formatage Prettier |
| `npm test` | Suite de tests (une seule exécution) |
| `npm run test:watch` | Tests en mode watch |

## Architecture

```
src/
  types/api.ts        types miroir des modèles Pydantic de app/api.py
  lib/
    api.ts             client HTTP typé (timeout, erreurs non-JSON gérées)
    ttlCache.ts         petit cache mémoire à TTL
    radar.ts, format.ts logique métier pure, testée indépendamment de l'UI
  hooks/
    useTeams.ts         charge la liste des équipes (mise en cache 5 min)
    usePrediction.ts     orchestre predict + stats des deux équipes
  components/
    ui/                 design system (Card, Button, Alert, Badge, Spinner…)
    layout/              Navbar, Hero, Footer
    match/                sélecteur d'équipes + garde-fou "équipes identiques"
    results/              boîte de prédiction, barre de probabilité, tableau
                          comparatif, radar, forme récente, évolution des buts
```

Les graphiques (Recharts) sont chargés à la demande (`React.lazy`) : ils ne font pas partie du bundle initial puisqu'ils ne sont nécessaires qu'après une prédiction.

## Déploiement sur Render

Ce projet compile en fichiers statiques (`dist/`). Deux façons de l'héberger sur Render :

### Option A — Static Site (le plus simple, gratuit, recommandé)

1. **New → Static Site**, pointer sur ce repo.
2. **Root Directory** : `frontend`
3. **Build Command** : `npm install && npm run build`
4. **Publish Directory** : `dist`
5. **Environment Variable** : `VITE_API_URL` = l'URL de votre service API (ex. `https://prediction-match.onrender.com`) — **sans slash final**.
6. Ajouter une règle de réécriture (Render → Redirects/Rewrites) : `/* → /index.html` (200), pour que les rechargements de page fonctionnent (SPA à point d'entrée unique).

Pas de "Start Command" avec ce type de service — Render sert les fichiers statiques directement.

### Option B — Web Service

Si le service est créé en tant que **Web Service** (le champ "Start Command" est visible), les fichiers doivent être servis par un petit process Node :

1. **Root Directory** : `frontend`
2. **Build Command** : `npm install && npm run build`
3. **Start Command** : `npm start` (lance `serve -s dist -l $PORT` — le flag `-s` gère le fallback SPA, équivalent à la règle de réécriture de l'option A)
4. **Environment Variable** : `VITE_API_URL` = l'URL de votre service API, **définie avant le build** — Vite fige `VITE_API_URL` dans le bundle au moment du build, elle n'est pas relue au démarrage du process.
