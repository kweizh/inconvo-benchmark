FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js and PostgreSQL client."

RUN mkdir -p /home/user/myproject

# Container contents:
#   - Node.js v24 for running the Inconvo script
#   - postgresql-client for initializing the initial state db
#   - /home/user/myproject base directory for the task

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
