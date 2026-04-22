FROM node:20-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment for tests
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install pytest psycopg2-binary requests

# Set up working directory
WORKDIR /app

# Pre-install common Node.js dependencies to speed up evaluation
RUN npm install -g express @inconvoai/node dotenv

# Copy task files if any (instruction.md will be provided by Harbor)
# COPY . .

# Initialize database schema (This would normally be done in a setup script or here)
# We assume DATABASE_URL is provided at runtime.
# We will create a small setup script to seed the database.
RUN echo "CREATE TABLE stores (id SERIAL PRIMARY KEY, name TEXT);" > /init.sql && \
    echo "CREATE TABLE products (id SERIAL PRIMARY KEY, store_id INTEGER REFERENCES stores(id), name TEXT, price DECIMAL);" >> /init.sql && \
    echo "CREATE TABLE orders (id SERIAL PRIMARY KEY, product_id INTEGER REFERENCES products(id), store_id INTEGER REFERENCES stores(id), amount INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);" >> /init.sql && \
    echo "INSERT INTO stores (name) VALUES ('Store A'), ('Store B');" >> /init.sql && \
    echo "INSERT INTO products (store_id, name, price) VALUES (1, 'Widget', 10.0), (2, 'Gadget', 20.0);" >> /init.sql && \
    echo "INSERT INTO orders (product_id, store_id, amount) VALUES (1, 1, 5), (2, 2, 3);" >> /init.sql

# Entrypoint will run the init script if DATABASE_URL is present
COPY <<EOF /entrypoint.sh
#!/bin/bash
if [ -n "\$DATABASE_URL" ]; then
    psql \$DATABASE_URL -f /init.sql
fi
exec "\$@"
EOF
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
