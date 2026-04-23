FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @getpochi/cli agent-browser inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial semantic model for sales."

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    cat >inconvo.yaml <<'EOF'
tables:
  sales:
    state: Queryable
    fields:
      id: { state: On }
      revenue: { state: On, type: measure }
      cost: { state: On, type: measure }
EOF

# Container contents:
#   - Node.js v24 installed
#   - inconvo CLI installed
#   - postgresql-client installed
#   - /home/user/inconvo-project - Inconvo project directory
#   - inconvo.yaml with initial sales table

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
