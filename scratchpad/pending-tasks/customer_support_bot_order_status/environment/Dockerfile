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
LABEL Description="Node.js environment with Inconvo project setup."

RUN mkdir -p /home/user/inconvo-bot && \
    cd /home/user/inconvo-bot && \
    cat > .env <<'EOF'
INCONVO_API_KEY=dummy_api_key
INCONVO_AGENT_ID=dummy_agent_id
DATABASE_URL=postgres://dummy:dummy@localhost:5432/dummy
EOF

# Container contents:
#   - Node.js v24 installed
#   - /home/user/inconvo-bot initialized with .env file containing required variables

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]