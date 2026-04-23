FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g inconvo@2.4.4 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial semantic model inconvo.yaml in /home/user/inconvo-project."

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
  customers:
    state: Queryable
    fields:
      name: { state: On }
  internal_logs:
    state: Queryable
    fields:
      log_id: { state: On }
      message: { state: On }
relations:
  - name: order_to_customer
    left: orders.customer_id
    right: customers.id
EOF

# Container contents:
#   - Node.js v24 and inconvo CLI installed.
#   - /home/user/inconvo-project — Inconvo project with initial config
#   - inconvo.yaml with all table states as Queryable

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]