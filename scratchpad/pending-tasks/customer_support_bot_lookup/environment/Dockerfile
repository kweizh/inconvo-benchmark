FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        postgresql-client postgresql postgresql-contrib \
        ffmpeg ripgrep libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 libxshmfence1 libgbm1 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @getpochi/cli agent-browser && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN agent-browser install

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with PostgreSQL and Node.js v24. Includes sample customer and order data."

# Initialize PostgreSQL and seed data
RUN service postgresql start && \
    su - postgres -c "psql -c \"CREATE USER user WITH PASSWORD 'password' SUPERUSER;\"" && \
    su - postgres -c "psql -c \"CREATE DATABASE support_db OWNER user;\"" && \
    su - postgres -c "psql -d support_db -c \"CREATE TABLE customers (id SERIAL PRIMARY KEY, name TEXT, email TEXT);\"" && \
    su - postgres -c "psql -d support_db -c \"CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), status TEXT, total_amount DECIMAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\"" && \
    su - postgres -c "psql -d support_db -c \"CREATE TABLE order_items (id SERIAL PRIMARY KEY, order_id INTEGER REFERENCES orders(id), product_name TEXT, quantity INTEGER, price DECIMAL);\"" && \
    su - postgres -c "psql -d support_db -c \"INSERT INTO customers (name, email) VALUES ('Alice Smith', 'alice@example.com');\"" && \
    su - postgres -c "psql -d support_db -c \"INSERT INTO orders (customer_id, status, total_amount) VALUES (1, 'shipped', 100.00);\"" && \
    su - postgres -c "psql -d support_db -c \"INSERT INTO order_items (order_id, product_name, quantity, price) VALUES (1, 'Widget', 2, 50.00);\"" && \
    service postgresql stop

ENV DATABASE_URL=postgresql://user:password@localhost:5432/support_db

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 and PostgreSQL
#   - Inconvo CLI (available via npx)
#   - Pre-populated database 'support_db' with customers and orders
#   - /home/user: base directory for the project

CMD ["/bin/bash", "-c", "service postgresql start && trap : TERM INT; sleep infinity & wait"]
