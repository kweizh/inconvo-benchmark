FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/inconvo-app && chmod 0755 /home/user /home/user/inconvo-app

LABEL Author="any-task-builder"
LABEL Description="Node.js v24 environment for Inconvo multi-tenant authorization task."

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/inconvo-app: empty project directory for the user to initialize.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
