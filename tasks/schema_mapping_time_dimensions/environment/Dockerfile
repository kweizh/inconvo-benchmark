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
LABEL Description="Inconvo task environment with Node.js v24 installed and an initial inconvo.yaml configuration."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install yaml && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
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

RUN cd /home/user/inconvo-app && \
    cat >index.js <<'EOF'
const fs = require('fs');
const yaml = require('yaml');

try {
    const file = fs.readFileSync('inconvo.yaml', 'utf8');
    const doc = yaml.parse(file);
    
    const createdAt = doc.tables?.orders?.fields?.created_at;
    if (createdAt && createdAt.state === 'On' && createdAt.type === 'dimension') {
        fs.writeFileSync('response.json', JSON.stringify({ table: [{ result: 'success' }] }));
        console.log('Configuration is valid. Time-based queries are now supported.');
        process.exit(0);
    } else {
        console.error('Configuration is invalid. created_at must have state: On and type: dimension');
        process.exit(1);
    }
} catch (e) {
    console.error('Error parsing inconvo.yaml:', e.message);
    process.exit(1);
}
EOF

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/inconvo-app — Inconvo project with initial inconvo.yaml and index.js
#   - inconvo.yaml with created_at missing the type: dimension configuration

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
