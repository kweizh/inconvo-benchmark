FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js v24 and PostgreSQL client."

# Container contents:
#   - Node.js v24
#   - PostgreSQL client (psql)
#   - Inconvo CLI will be used via npx by the agent

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
