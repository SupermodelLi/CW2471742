```md
# Flask Horror Story Generator (API + HTML Frontend)

An integrated Flask app that generates horror stories via a JSON API and serves an interactive HTML frontend from the same server. Includes presets, location suggestions, story history, share/report flows, and basic moderation endpoints. CORS is enabled for API use.

## Setup

```bash
pip install flask flask-cors
```

## Run

```bash
python main.py
```

## Access

Open the app in your browser:
- http://127.0.0.1:5005

The interactive HTML frontend is served automatically from:
- `GET /` (and static assets via `GET /<path:filename>`)

## API Endpoints

- Health: `GET /health`
- Location suggestions: `GET /api/locations/suggest`
- Generate story: `POST /api/generate`
- Presets: `GET /api/presets`
- Custom generation: `POST /api/generate/custom`
- Story list/history: `GET /api/stories`
- Share a story: `POST /api/stories/<story_id>/share`
- Report a story: `POST /api/stories/<story_id>/report`
- Moderation reports: `GET /mod/reports`
- Moderation action: `POST /mod/stories/<story_id>/action`

## cURL Examples

Health check:
```bash
curl http://127.0.0.1:5005/health
```

Generate a story:
```bash
curl -X POST http://127.0.0.1:5005/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A lighthouse keeper hears footsteps above the lantern room.","preset":"classic"}'
```
```