FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash libpq-dev gcc python3-dev && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages psycopg2-binary pytest

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js v24 and Python 3 installed."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    npm init -y && \
    npm install @inconvoai/node dotenv && \
    npm install -g inconvo

# Container contents:
#   - Node.js v24 installed
#   - Python 3 with psycopg2-binary and pytest
#   - inconvo CLI installed globally
#   - /home/user/project - basic Node.js project for Inconvo

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]