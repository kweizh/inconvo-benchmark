FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-yaml python3-psycopg2 bash \
        postgresql postgresql-contrib sudo && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setup user and directory
RUN mkdir -p /home/user && chmod 0755 /home/user
WORKDIR /home/user

# Configure PostgreSQL
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER inconvo WITH SUPERUSER PASSWORD 'inconvo';" && \
    createdb -O inconvo inconvo_db && \
    psql -d inconvo_db -c "CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(255));" && \
    psql -d inconvo_db -c "CREATE TABLE line_items (id SERIAL PRIMARY KEY, product_id INT REFERENCES products(id), quantity INT);" && \
    psql -d inconvo_db -c "INSERT INTO products (name) VALUES ('Widget'), ('Gadget');" && \
    psql -d inconvo_db -c "INSERT INTO line_items (product_id, quantity) VALUES (1, 10), (2, 5), (1, 2);" && \
    /etc/init.d/postgresql stop
USER root

# Create the project directory and initial inconvo.yaml
RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    cat >inconvo.yaml <<'EOF'
tables:
  products:
    state: Off
    fields:
      id: { state: Off }
      name: { state: Off }
  line_items:
    state: Off
    fields:
      id: { state: Off }
      product_id: { state: Off }
      quantity: { state: Off }
relations: []
EOF

ENV DATABASE_URL="postgresql://inconvo:inconvo@localhost:5432/inconvo_db"

# Ensure postgres starts on container start
CMD ["/bin/bash", "-c", "service postgresql start && trap : TERM INT; sleep infinity & wait"]
