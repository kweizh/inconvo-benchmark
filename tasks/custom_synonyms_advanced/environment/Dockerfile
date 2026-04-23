FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-yaml bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml semantic model."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    cat > inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
      created_at: { state: On, type: dimension }
  customers:
    state: Joinable
    fields:
      name: { state: On }
relations:
  - name: order_to_customer
    left: orders.customer_id
    right: customers.id
EOF

# Container contents:
#   - Node.js v24 and python3-yaml installed
#   - inconvo CLI installed via npm
#   - /home/user/project  — Inconvo project with initial inconvo.yaml

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
