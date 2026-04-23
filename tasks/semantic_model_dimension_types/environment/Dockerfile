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
LABEL Description="Inconvo project with an initial inconvo.yaml config in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On }
      created_at: { state: On }
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
#   - Node.js v24 and inconvo CLI installed globally.
#   - /home/user/myproject  — inconvo project with initial config
#   - inconvo.yaml with orders table but missing dimension/measure types for total_amount and created_at.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]