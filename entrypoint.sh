#!/bin/sh

echo "──────────────────────────────────────"
echo " CodeBoost - Starting up..."
echo "──────────────────────────────────────"

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.5
done
echo "✅ PostgreSQL is ready!"

# Run migrations (same as Render build command)
echo "📦 Running makemigrations..."
python manage.py makemigrations --noinput

echo "📦 Running migrate..."
python manage.py migrate --noinput

echo "🗑 Removing old static files..."
rm -rf /app/static

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Daphne..."
exec "$@"
