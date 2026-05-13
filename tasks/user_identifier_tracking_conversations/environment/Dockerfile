FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js v24 environment with @inconvoai/node SDK pre-installed and users.json containing two end-user identifiers."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install @inconvoai/node dotenv && \
    printf '%s' '["alice-001","bob-002"]' > /home/user/inconvo-app/users.json

# Container contents:
#   - Node.js v24 (via NodeSource)
#   - /home/user/inconvo-app: initialised npm project with @inconvoai/node and dotenv installed
#   - /home/user/inconvo-app/users.json: JSON array of end-user identifiers ["alice-001","bob-002"]

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
