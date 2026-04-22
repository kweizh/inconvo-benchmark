FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Inconvo CLI
RUN npm install -g inconvo@latest

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project environment for schema hardening and column visibility task."

# Setup the project
RUN mkdir -p /home/user/inconvo-project/.inconvo && \
    cd /home/user/inconvo-project && \
    cat > .inconvo/inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      email: { state: On, type: dimension }
      password_hash: { state: On, type: dimension }
      secret_key: { state: On, type: dimension }
      created_at: { state: On, type: dimension }
  orders:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      user_id: { state: On, type: dimension }
      amount: { state: On, type: measure }
relations:
  - name: user_orders
    left: users.id
    right: orders.user_id
EOF

# Container contents:
#   - python3, python3-pytest, bash, postgresql-client
#   - Node.js v24 and Inconvo CLI
#   - /home/user/inconvo-project: Pre-initialized Inconvo project with a semantic model
#   - .inconvo/inconvo.yaml: Initial semantic model with sensitive columns visible

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
