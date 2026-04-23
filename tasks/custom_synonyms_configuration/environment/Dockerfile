FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml configuration in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
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
#   - Node.js v24 and npm installed.
#   - inconvo CLI installed globally.
#   - /home/user/myproject: Inconvo project directory.
#   - inconvo.yaml with orders table and total_amount field, but no synonyms.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
