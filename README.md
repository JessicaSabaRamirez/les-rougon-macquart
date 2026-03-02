# Les Rougon-Macquart — Companion App

An interactive companion to Émile Zola's twenty-novel cycle *Les Rougon-Macquart* (1871–1893).

## Quick Start (local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database
python data/seed.py

# 3. Run the app
uvicorn app.main:app --reload --port 8080
```

Open http://localhost:8080

## Docker (local)

```bash
docker-compose up --build
```

## Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```
rougon-macquart/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # DB connection
│   ├── routers/             # characters, novels, locations, search
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, images
├── data/
│   ├── seed.py              # Database seeding script
│   └── rougon_macquart.db   # SQLite database (created by seed.py)
├── tests/
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Deploying to Google Cloud Run — Step-by-Step

This app uses SQLite seeded at Docker build time (no external database required).
The image is stateless from Cloud Run's perspective: each deployment bakes in a fresh database.

### Prerequisites

- A Google account
- A Google Cloud project (create one at https://console.cloud.google.com)
- Billing enabled on the project (Cloud Run has a generous free tier)
- The [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed on your machine

### Step 1 — Install and configure gcloud

```bash
# Install gcloud (macOS with Homebrew)
brew install --cask google-cloud-sdk

# Or on Windows: download the installer from https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# Set a default region (europe-west1 is Switzerland — good for EU data)
gcloud config set run/region us-west1
```

### Step 2 — Enable required APIs

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com
```

This only needs to be done once per project.

### Step 3 — Create an Artifact Registry repository

Cloud Run uses Artifact Registry (the modern replacement for Container Registry).

```bash
gcloud artifacts repositories create les-rougon-macquart --repository-format=docker --location=us-west1 --description="Les Rougon-Macquart companion app"
```

Set up Docker authentication for the registry:

```bash
gcloud auth configure-docker us-west1-docker.pkg.dev
```

Grant the Cloud Build service account permission to push to Artifact Registry
(replace YOUR_PROJECT_NUMBER — find it with `gcloud projects describe YOUR_PROJECT_ID`):

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_NUMBER \
  --member="serviceAccount:YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

This is a one-time setup per project.

### Step 4 — Build and push the Docker image

From the project root directory (where `Dockerfile` lives):

```bash
# Image path — use the project ID (not project number) in the Artifact Registry URL
IMAGE=us-west1-docker.pkg.dev/les-rougon-macquart/les-rougon-macquart/app:latest

# Build with Cloud Build (runs in the cloud, no local Docker required)
gcloud builds submit --tag $IMAGE

# --- OR build locally and push (requires Docker Desktop running) ---
# docker build -t $IMAGE .
# docker push $IMAGE
```

Cloud Build is recommended — it's faster, runs in Google's infrastructure, and
you don't need Docker running locally.

### Step 5 — Deploy to Cloud Run

```bash
gcloud run deploy les-rougon-macquart --image us-west1-docker.pkg.dev/les-rougon-macquart/les-rougon-macquart/app:latest --platform managed --region us-west1 --allow-unauthenticated --memory 256Mi --cpu 1 --min-instances 0 --max-instances 3 --port 8080
```

Flags explained:
- `--allow-unauthenticated` — public access (needed for a personal website)
- `--memory 256Mi` — sufficient for this app; can raise to 512Mi if needed
- `--min-instances 0` — scales to zero when not in use (saves cost)
- `--max-instances 3` — prevents runaway scaling

Cloud Run will print the service URL when done, e.g.:
```
Service URL: https://rougon-macquart-xxxxxxxxxx-ew.a.run.app
```

### Step 6 — Verify the deployment

```bash
# Open in browser
gcloud run services describe rougon-macquart --region europe-west1 \
  --format 'value(status.url)' | xargs open

# Or check the health endpoint
curl https://YOUR_SERVICE_URL/health
# Should return: {"status": "ok"}
```

### Step 7 (optional) — Set up a custom domain

If you have a domain (e.g. via Namecheap, Google Domains, etc.):

```bash
# Map the domain
gcloud run domain-mappings create \
  --service rougon-macquart \
  --domain your-domain.com \
  --region europe-west1
```

Then add the DNS records shown in the output to your domain registrar.

### Re-deploying after code changes

Each time you update the app (new characters, bug fixes, etc.):

```bash
IMAGE=us-west1-docker.pkg.dev/les-rougon-macquart/les-rougon-macquart/app:latest

# Rebuild and push
gcloud builds submit --tag $IMAGE

# Deploy new revision
gcloud run deploy les-rougon-macquart \
  --image $IMAGE \
  --region us-west1
```

Cloud Run performs zero-downtime deployments — the old revision keeps serving
traffic until the new one is healthy.

### Cost estimate

For a personal reading companion with occasional traffic:
- **Cloud Run**: Free tier covers 2M requests/month, 360K GB-seconds/month.
  A personal site will likely stay entirely within the free tier.
- **Cloud Build**: 120 build-minutes/day free (each build takes ~2–3 minutes).
- **Artifact Registry**: First 0.5 GB/month free; the image is ~200MB.

**Effective cost: $0/month** for typical personal use.

---

## Features (current)
- **Genealogy tree** — interactive SVG family tree on the landing page
- **Character directory** — ~60 characters with branch filter, portrait thumbnails, descriptions
- **Character profiles** — full page with family relations, novel appearances, physical description
- **Novel index** — all 20 novels with summaries (EN/FR)
- **Novel profiles** — major and minor characters per novel
- **Atlas** — key locations across France with descriptions
- **Search** — full-text search across characters, novels, and locations
- **EN/FR toggle** — all content available in English and French

## Roadmap
- [x] Timeline of historical and personal events
- [x] Quote browser
- [x] Favicon (small SVG in parchment/gold style)
- [ ] More character portrait images
- [ ] Full family tree — all ~60 characters (not just featured ones), with zoom/pan navigation so the full tree is explorable
- [ ] Much more data — longer character biographies with physical descriptions and character arcs, fuller novel summaries, more timeline events, more locations with maps/images; the database content is the heart of the app
- [ ] Better image display — smart thumbnail cropping so the focal point of each image shows in list/card views; portrait images embedded in family tree nodes
- [ ] Spoiler level filter (based on reading progress)
- [ ] Custom domain
