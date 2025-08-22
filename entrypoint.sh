#!/usr/bin/env bash
set -e

echo "⏳ Checking database availability..."

python <<'PY'
import os, time, psycopg
dsn = os.getenv("DATABASE_URL")
if not dsn:
    dsn = f"postgresql://{os.getenv('DB_USER','jobboard')}:{os.getenv('DB_PASSWORD','secret')}@" \
          f"{os.getenv('DB_HOST','db')}:{os.getenv('DB_PORT','5432')}/{os.getenv('DB_NAME','jobboard')}"
for i in range(60):
    try:
        with psycopg.connect(dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        print("✅ Database is ready!")
        break
    except Exception:
        print(f"⏳ Waiting for DB... attempt {i+1}/60")
        time.sleep(1)
else:
    raise SystemExit("❌ Database not reachable after 60s")
PY

# In dev, also run makemigrations
if [ "${DJANGO_DEBUG:-1}" = "1" ]; then
  echo "🛠 Running makemigrations (dev only)..."
  uv run python manage.py makemigrations --noinput
fi

echo "📦 Applying migrations..."
uv run python manage.py migrate --noinput

if [ "${DJANGO_COLLECTSTATIC:-0}" = "1" ]; then
  echo "📂 Collecting static files..."
  uv run python manage.py collectstatic --noinput
fi

if [ "${DJANGO_DEBUG:-1}" = "1" ]; then
  echo "🚀 Starting Django development server..."
  exec uv run python manage.py runserver 0.0.0.0:8000
else
  echo "🚀 Starting Gunicorn (production)..."
  exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=${GUNICORN_WORKERS:-3}
fi
