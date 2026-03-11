# Deploy persona-platform til Railway via GitHub

## Forudsætninger
- GitHub repo: `sini12345/persona-platform` (FastAPI app)
- Railway konto: [railway.app](https://railway.app)
- Anthropic API key: [console.anthropic.com](https://console.anthropic.com)

## Trin 1: Opret Railway-projekt

1. Log ind på [railway.app](https://railway.app)
2. Klik **"New Project"** → **"Deploy from GitHub Repo"**
3. Autoriser Railway til at tilgå `sini12345/persona-platform`
4. Vælg repo → Railway detekterer automatisk `railway.toml`
5. Første deploy starter automatisk

## Trin 2: Tilføj Volume for SQLite-persistens

**KRITISK** — uden volume forsvinder databasen ved hver deploy.

1. I Railway dashboard: Klik på web-servicen
2. **"Settings"** → **"Volumes"** → **"Add Volume"**
3. Mount path: `/data`
4. Size: 1 GB er rigeligt

## Trin 3: Sæt environment variables

I Railway dashboard → Service → **"Variables"**:

| Variable | Beskrivelse | Påkrævet |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Din Anthropic API-nøgle | Ja |
| `ADMIN_PASSWORD` | Admin-password til holdkode-administration | Anbefalet |
| `SESSION_SECRET` | Tilfældig streng for cookie-sikkerhed | Anbefalet |

`PORT` sættes automatisk af Railway.

## Trin 4: Generer domæne

1. Service → **"Settings"** → **"Networking"**
2. Klik **"Generate Domain"** → får `*.up.railway.app` URL
3. Eller tilføj eget custom domain

## Verifikation

1. Tjek deploy-logs i Railway for fejl
2. `https://<din-app>.up.railway.app/health` → `{"status": "ok"}`
3. Gå til `/` → Login med holdkode `TEST2026`
4. Vælg persona → scenario → mission → start samtale
5. Verificér at SSE streaming chat virker

## Automatisk deploy

Railway deployer automatisk ved push til `master`-branchen. Ingen yderligere CI/CD opsætning nødvendig.

## Eksisterende konfiguration

Repo'et har allerede:
- `railway.toml` — nixpacks builder, healthcheck, restart policy
- `Procfile` — `web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`
- `requirements.txt` — alle Python dependencies med pinned versions
- `/health` endpoint — healthcheck route
- SQLite database path der understøtter Railway (`/data/persona.db`)
