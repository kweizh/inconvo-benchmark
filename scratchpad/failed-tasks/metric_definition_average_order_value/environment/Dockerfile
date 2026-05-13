FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project && chmod 0755 /home/user/project

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js v24 and Inconvo CLI installed."

# Container contents:
#   - system dependencies: curl ca-certificates git python3 python3-pip python3-pytest bash postgresql-client
#   - Node.js v24 and inconvo CLI
#   - /home/user/project: empty project directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
