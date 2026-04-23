FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-yaml postgresql-client bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial semantic model containing a products table."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >inconvo.yaml <<'EOF'
tables:
  products:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      price: { state: On, type: measure }
      cost: { state: On, type: measure }
EOF

RUN cat >/tmp/init_db.sql <<'EOF'
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL
);

INSERT INTO products (name, price, cost) VALUES
('Widget A', 100.00, 60.00),
('Widget B', 200.00, 150.00);
EOF

RUN cat >/tmp/setup.sh <<'EOF'
#!/bin/bash
set -e

until psql "$DATABASE_URL" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing init_db.sql"
psql "$DATABASE_URL" -f /tmp/init_db.sql
EOF
RUN chmod +x /tmp/setup.sh

# Container contents:
#   - Node.js v24 and inconvo CLI installed globally.
#   - /home/user/myproject - Inconvo project with initial inconvo.yaml
#   - inconvo.yaml with products table but no gross_margin computed column.
#   - /tmp/init_db.sql and /tmp/setup.sh to initialize the database

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
