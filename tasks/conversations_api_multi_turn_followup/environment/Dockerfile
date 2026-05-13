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
LABEL Description="Node.js environment with a pre-initialized Inconvo project (@inconvoai/node + dotenv installed) for multi-turn conversation tasks."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    cat > package.json <<'EOF'
{
  "name": "inconvo-app",
  "version": "1.0.0",
  "private": true,
  "main": "index.js",
  "dependencies": {
    "@inconvoai/node": "^0.8.0",
    "dotenv": "^16.4.5"
  }
}
EOF

RUN cd /home/user/inconvo-app && \
    cat > .env <<'EOF'
INCONVO_API_KEY=${INCONVO_API_KEY}
INCONVO_AGENT_ID=${INCONVO_AGENT_ID}
INCONVO_DB_URL=${INCONVO_DB_URL}
EOF

RUN cd /home/user/inconvo-app && \
    npm install --no-audit --no-fund

# Container contents:
#   - Node.js v24 installed
#   - /home/user/inconvo-app: pre-initialized project with package.json, .env, and node_modules
#   - @inconvoai/node and dotenv installed and ready to use
#   - .env references INCONVO_API_KEY, INCONVO_AGENT_ID, INCONVO_DB_URL (resolved at runtime)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
