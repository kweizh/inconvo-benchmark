FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo@latest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo task environment with Node.js v24, postgresql-client, and a pre-initialized inconvo project."

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    npm init -y && \
    npm install @inconvoai/node dotenv && \
    cat >inconvo.yaml <<'EOF'
tables:
  customers:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      name: { state: On, type: dimension }
  customer_addresses:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      customer_id: { state: On, type: dimension }
      city: { state: On, type: dimension }
relations: []
EOF

# Container contents:
#   - Node.js v24 and npm
#   - postgresql-client (psql)
#   - inconvo CLI installed globally
#   - /home/user/inconvo-project with an initial inconvo.yaml and dependencies

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
