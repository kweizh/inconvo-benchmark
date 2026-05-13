FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js v24, postgresql-client, and inconvo CLI installed."

RUN mkdir -p /home/user/myproject

# Container contents:
#   - python3, python3-pytest, bash, curl, wget, ca-certificates, git
#   - postgresql-client for initial state test
#   - Node.js v24 and npm
#   - inconvo CLI installed globally
#   - /home/user/myproject directory created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]