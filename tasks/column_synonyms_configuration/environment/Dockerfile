FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g inconvo

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml semantic model."

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    cat >inconvo.yaml <<'EOF'
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
#   - Node.js 24 and inconvo CLI installed.
#   - /home/user/inconvo-project  — Inconvo project directory
#   - inconvo.yaml with an orders table and total_amount field

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]