#!/bin/sh

# Exit script on any error
set -e

echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is up and running."

# Run database migrations (if using Alembic)
echo "Applying database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
exec "$@"
