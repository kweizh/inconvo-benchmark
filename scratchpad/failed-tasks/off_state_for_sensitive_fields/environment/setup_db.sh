#!/bin/bash
set -e

if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL is not set. Skipping DB setup."
  exit 0
fi

echo "Setting up database..."
psql "$DATABASE_URL" <<EOF
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    secret_key TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL
);

INSERT INTO users (username, password_hash, secret_key) VALUES ('admin', 'hashed_pass', 'super_secret') ON CONFLICT DO NOTHING;
EOF

echo "Database setup complete."
