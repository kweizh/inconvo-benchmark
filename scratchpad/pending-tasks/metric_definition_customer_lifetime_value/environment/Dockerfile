FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js and PostgreSQL client."

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    npm init -y && \
    npm install inconvo @inconvoai/node dotenv

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - postgresql-client for initial state tests
#   - Node.js v24 for running Inconvo CLI
#   - /home/user/inconvo-project: pre-initialized with inconvo dependencies

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]