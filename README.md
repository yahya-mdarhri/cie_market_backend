# cie_market_backend

Backend API for CIE Market (Django + PostgreSQL).

## Quick Start (local)

1) Create `.env` from `.env.example` and fill values.
2) Install dependencies.
3) Run migrations and start the server.

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Environment Variables

Required (minimum):
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `ALLOWED_HOSTS`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `JWT_SECRET`, `JWT_ALGORITHM`

Optional (if using `DATABASE_URL` instead of individual DB vars):
- `DATABASE_URL`
- `DB_CONN_MAX_AGE`
- `DB_SSL_REQUIRE`

Storage (S3-compatible):
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_ENDPOINT_URL`
- `AWS_S3_REGION_NAME`
- `AWS_S3_ADDRESSING_STYLE`

## Docker

Build and run:

```powershell
docker build -f dockerfile -t cie_market_backend .
docker run --env-file .env -p 8000:8000 cie_market_backend
```

Using compose:

```powershell
docker compose up --build
```

## Database Restore (example)

```bash
sudo -i -u postgres
/usr/lib/postgresql/16/bin/pg_restore -d inn2market --no-owner --no-acl /home/innmarket/stackhero.dump
```

## Collect static

```powershell
python manage.py collectstatic --noinput
```
