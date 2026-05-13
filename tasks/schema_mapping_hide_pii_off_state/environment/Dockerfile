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
LABEL Description="Inconvo project with PII fields (customers.email, customers.phone) initially exposed via state: On in inconvo.yaml."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm pkg set type=module && \
    npm install @inconvoai/node && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
      created_at: { state: On, type: dimension }
      customer_id: { state: On }
  customers:
    state: Queryable
    fields:
      id: { state: On }
      name: { state: On }
      email: { state: On }
      phone: { state: On }
relations:
  - name: order_to_customer
    left: orders.customer_id
    right: customers.id
EOF

# Container contents:
#   - always required libs: curl wget ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for running the Inconvo SDK script
#   - /home/user/inconvo-app: pre-initialized npm project (type=module) with @inconvoai/node installed
#   - /home/user/inconvo-app/inconvo.yaml: semantic model with customers.email and customers.phone set to state: On

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
