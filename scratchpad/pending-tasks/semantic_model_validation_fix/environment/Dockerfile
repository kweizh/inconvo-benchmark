FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        postgresql-client libpq-dev && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages psycopg2-binary pytest pyyaml

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo semantic model validation fix task environment"

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    cat >inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      name: { state: On, type: dimension }
  orders:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      user_id: { state: On, type: dimension }
      amount: { state: On, type: measure }
  payments:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      order_id: { state: On, type: dimension }
      user_id: { state: On, type: dimension }
      amount: { state: On, type: measure }
relations:
  - name: payment_to_user_direct
    left: payments.user_id
    right: users.id
  - name: payment_to_order
    left: payments.order_id
    right: orders.id
  - name: order_to_user
    left: orders.user_id
    right: users.id
  # Intentional syntax error below (indentation/structure)
  - name: ambiguous_path
  left: payments.user_id
   right: users.id
EOF

RUN touch /home/user/inconvo-project/.env

# Container contents:
#   - Node.js v24 and Inconvo CLI installed
#   - Python 3 with pytest and psycopg2-binary
#   - /home/user/inconvo-project with invalid inconvo.yaml and empty .env file

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
