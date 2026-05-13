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
LABEL Description="Node.js v24 environment with @inconvoai/node SDK pre-installed for streaming Data Agent responses."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    cat > package.json <<'EOF'
{
  "name": "inconvo-app",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "description": "Streaming Inconvo Data Agent response task.",
  "main": "index.js",
  "dependencies": {
    "@inconvoai/node": "^0.8.0",
    "dotenv": "^16.4.5"
  }
}
EOF

RUN cd /home/user/inconvo-app && npm install --no-audit --no-fund

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for running the Inconvo SDK script
#   - /home/user/inconvo-app: Node.js project pre-configured with @inconvoai/node and dotenv
#     and node_modules already installed (npm install must NOT be re-run by the agent)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
