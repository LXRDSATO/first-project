# Micro-Tours Darija MVP

Automated Moroccan micro-tour video generator using Python, FastAPI, TTS, and AI.

## Structure

- `backend/` – API, scripts, tests, config
- `frontend/pages/` – Generated HTML landing pages
- `deployment/` – Docker, deployment scripts
- `docs/` – Documentation

## Quick Start

1. See `deployment/` for Docker Compose setup
2. Backend: FastAPI, Celery, SQLite
3. Frontend: Static HTML pages

## Usage Example

Generate a micro-tour via API:

```bash
curl -X POST http://localhost:8000/generate_microtour \
  -H "Content-Type: application/json" \
  -d '{"place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA", "category": "cafe", "city": "طنجة"}'
```

Response includes spot info, script, images, video, and landing page path.

## API Endpoints

- `GET /` – Health check
- `POST /generate_microtour` – Generate a micro-tour (see above)

## Environment Setup

1. Copy `.env.example` to `backend/config/.env` and fill in your API keys.
2. Run with Docker Compose:

   ```bash
   cd deployment
   docker-compose up --build
   ```

## Health & Maintenance

- Add your API keys to `.env` (never commit real secrets)
- Static files (videos, images, review) are output to `frontend/pages/`
- For production, secure the API and add rate limiting

---

For more, see the full project prompt in `docs/`.
