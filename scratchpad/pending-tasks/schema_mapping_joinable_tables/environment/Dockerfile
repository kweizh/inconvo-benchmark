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
LABEL Description="Inconvo project with an initial inconvo.yaml configuring customers as Queryable."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install @inconvoai/node dotenv && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
      created_at: { state: On, type: dimension }
  customers:
    state: Queryable
    fields:
      name: { state: On }
relations:
  - name: order_to_customer
    left: orders.customer_id
    right: customers.id
EOF

RUN cd /home/user/inconvo-app && \
    cat >index.js <<'EOF'
const fs = require('fs');
// Mocking the inconvo sdk response for the test
const data = {
  table: {
    rows: [
      { id: 1, total_amount: 100, name: "Alice" }
    ]
  }
};
fs.writeFileSync('response.json', JSON.stringify(data));
console.log('Saved response.json');
EOF

# Container contents:
#   - Node.js v24 installed.
#   - @inconvoai/node and dotenv installed in /home/user/inconvo-app.
#   - /home/user/inconvo-app/inconvo.yaml with customers configured as Queryable.
#   - /home/user/inconvo-app/index.js mock script.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
