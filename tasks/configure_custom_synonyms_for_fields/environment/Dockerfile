FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql postgresql-contrib && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo@latest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml config in /home/user/myproject and a PostgreSQL database."

# Setup PostgreSQL
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER testuser WITH SUPERUSER PASSWORD 'testpass';" && \
    createdb -O testuser testdb && \
    psql -d testdb -c "CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(100), dob DATE);" && \
    psql -d testdb -c "INSERT INTO customers (name, dob) VALUES ('Alice', '1990-01-01');"

USER root

ENV DATABASE_URL="postgresql://testuser:testpass@localhost:5432/testdb"

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >inconvo.yaml <<'EOF'
tables:
  customers:
    state: Queryable
    fields:
      id: { state: On }
      name: { state: On }
      dob: { state: On }
EOF

# Container contents:
#   - Node.js v24 and inconvo CLI installed.
#   - PostgreSQL installed and running with testdb.
#   - /home/user/myproject  — inconvo project with initial config
#   - inconvo.yaml with customers table and dob field without synonyms.

CMD ["/bin/bash", "-c", "/etc/init.d/postgresql start && trap : TERM INT && sleep infinity & wait"]