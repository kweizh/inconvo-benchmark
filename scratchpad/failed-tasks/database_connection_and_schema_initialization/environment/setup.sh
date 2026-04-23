#!/bin/bash
set -e

if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL is not set"
  exit 1
fi

echo "Initializing database schema..."
psql "$DATABASE_URL" -f /app/init_db.sql

echo "Database initialized."
