FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        postgresql postgresql-contrib sudo && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo@latest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages pyyaml

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with PostgreSQL and Node.js v24 installed."

RUN service postgresql start && \
    su - postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\"" && \
    su - postgres -c "createdb inconvo" && \
    su - postgres -c "psql -d inconvo -c \"CREATE TABLE users (id SERIAL PRIMARY KEY, last_login DATE);\""

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On }
      last_login: { state: On, type: dimension }
EOF

# Container contents:
#   - Node.js v24 and Inconvo CLI
#   - PostgreSQL installed and configured with the 'inconvo' database
#   - /home/user/myproject  — mytool project with initial config
#   - inconvo.yaml with users table

CMD ["/bin/bash", "-c", "trap : TERM INT; service postgresql start && sleep infinity & wait"]
