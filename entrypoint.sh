#!/usr/bin/env sh
set -e

python manage.py migrate --noinput

if [ "${DJANGO_COLLECTSTATIC:-1}" = "1" ]; then
  python manage.py collectstatic --noinput
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
