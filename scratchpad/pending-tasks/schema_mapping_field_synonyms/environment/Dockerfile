FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo Node.js project pre-installed at /home/user/inconvo-app with @inconvoai/node, dotenv, and a starter inconvo.yaml that has no synonyms yet."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install @inconvoai/node dotenv

RUN cat > /home/user/inconvo-app/inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      customer_id: { state: On }
      total_amount: { state: On, type: measure }
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

# Container contents:
#   - System: curl wget ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 from NodeSource
#   - /home/user/inconvo-app: pre-initialized Node project with @inconvoai/node and dotenv installed
#   - /home/user/inconvo-app/inconvo.yaml: starter semantic model with `orders` (Queryable)
#     and `customers` (Joinable) tables, a join relation, but NO synonyms yet.
#   - Real INCONVO_API_KEY / INCONVO_AGENT_ID / INCONVO_DB_URL env vars are injected at runtime by Harbor.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
