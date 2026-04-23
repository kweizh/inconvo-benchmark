FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-yaml bash \
        postgresql postgresql-contrib sudo && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with PostgreSQL running"

RUN service postgresql start && \
    su - postgres -c "psql -c \"CREATE USER inconvo WITH SUPERUSER PASSWORD 'inconvo';\"" && \
    su - postgres -c "createdb -O inconvo inconvo_db" && \
    su - postgres -c "psql -d inconvo_db -c \"CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255));\""

RUN mkdir -p /home/user/myproject

# Container contents:
#   - Node.js v24 and inconvo CLI installed
#   - PostgreSQL running with inconvo_db database
#   - /home/user/myproject directory ready for initialization

CMD ["/bin/bash", "-c", "trap : TERM INT; service postgresql start && sleep infinity & wait"]