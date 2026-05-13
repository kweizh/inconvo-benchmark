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
LABEL Description="Inconvo project pre-seeded with starter inconvo.yaml (orders + customers) and @inconvoai/node installed; gross_margin measure not yet defined."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install @inconvoai/node dotenv

RUN cd /home/user/inconvo-app && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      customer_id: { state: On }
      total_amount: { state: On, type: measure }
      cost: { state: On, type: measure }
      created_at: { state: On, type: dimension }
  customers:
    state: Joinable
    fields:
      id: { state: On }
      name: { state: On }
relations:
  - name: order_to_customer
    left: orders.customer_id
    right: customers.id
EOF

RUN cd /home/user/inconvo-app && \
    cat >.env <<'EOF'
INCONVO_API_KEY=
INCONVO_AGENT_ID=
INCONVO_DB_URL=
EOF

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 installed via NodeSource
#   - /home/user/inconvo-app: Node.js project with @inconvoai/node and dotenv installed
#   - /home/user/inconvo-app/inconvo.yaml: starter semantic model with `orders` (Queryable) and `customers` (Joinable); no gross_margin measure yet
#   - /home/user/inconvo-app/.env: placeholders for INCONVO_API_KEY / INCONVO_AGENT_ID / INCONVO_DB_URL (real values supplied at runtime via env)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
