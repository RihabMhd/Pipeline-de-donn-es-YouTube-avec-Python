# Pipeline ELT YouTube — Airflow / Docker / PostgreSQL

Pipeline d'extraction et de transformation de données YouTube, orchestré avec Apache Airflow (LocalExecutor) et PostgreSQL, entièrement conteneurisé avec Docker Compose.

## Architecture

**DAG 1 — `youtube_extraction`** (schedule: `@daily`)
1. `extract_playlist` — récupère la liste des vidéos de la chaîne via l'API YouTube (`get_playlist.py`)
2. `get_video_details` — récupère les détails (durée, vues, likes, commentaires) et génère le JSON (`get_video_details.py`)
3. `trigger_dwh_update` — déclenche le DAG 2 (`TriggerDagRunOperator`)

**DAG 2 — `youtube_dwh_update`** (schedule: déclenché uniquement par DAG 1)
1. `load_staging` — charge le JSON dans `staging.videos` (upsert + delete des lignes obsolètes)
2. `transform_core` — transforme et charge les données vers `core.videos`

## Stack

- Airflow Webserver + Scheduler (LocalExecutor)
- PostgreSQL 13 (metadata Airflow + base ELT)
- Docker Compose

## Transformations appliquées (staging → core)

| Transformation | Détail |
|---|---|
| Conversion des durées | ISO 8601 (`PT21S`) → secondes (via `isodate`) |
| Conversion des types | `view_count`/`like_count`/`comment_count` (texte) → `BIGINT` |
| Traitement des dates | ISO 8601 UTC → `TIMESTAMP` |
| Valeurs manquantes | `title` NULL/vide → `"Untitled"` |
| Colonnes calculées | `engagement_rate`, `like_view_ratio` (arrondis à 6 décimales) |
| Infos utiles à l'analyse | `duration_category` (short/medium/long), `publish_weekday` |

## Démarrage

```bash
docker compose up --build
```

Airflow UI : http://localhost:8080

Unpause les deux DAGs, puis déclencher `youtube_extraction` (le DAG 2 se lance automatiquement à la fin).

## Gestion des secrets

Toutes les informations sensibles (clé API, mots de passe, connexions DB) sont dans `.env`, exclu du dépôt via `.gitignore`. Aucun secret n'est commité sur GitHub.

## Tests effectués

- ✅ Réponse API YouTube (status 200) et pagination (31 pages, 1526 vidéos)
- ✅ Génération du JSON (`YT_data_{date}.json`)
- ✅ Création des schémas/tables `staging.videos` et `core.videos`
- ✅ Chargement des données en staging
- ✅ Application des 6 transformations, vérifiées sur données réelles
- ✅ INSERT / UPDATE (`ON CONFLICT`) et DELETE (lignes obsolètes) fonctionnels sur les deux tables
- ✅ Exécution complète des deux DAGs (succès, cascade DAG1 → DAG2)
- ✅ Environnement fonctionnel via `docker compose up` sans installation manuelle