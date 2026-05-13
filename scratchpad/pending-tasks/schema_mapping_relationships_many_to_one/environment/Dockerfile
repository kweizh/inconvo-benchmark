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
LABEL Description="Inconvo project environment with initial inconvo.yaml and index.js."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm i @inconvoai/node dotenv && \
    cat >inconvo.yaml <<'INNER_EOF'
tables:
  line_items:
    state: Queryable
    fields:
      id: { state: On }
      product_id: { state: On }
      quantity: { state: On, type: measure }
  products:
    state: Joinable
    fields:
      id: { state: On }
      name: { state: On }
INNER_EOF

RUN cd /home/user/inconvo-app && \
    cat >index.js <<'INNER_EOF'
const fs = require('fs');
const yaml = fs.readFileSync('inconvo.yaml', 'utf8');
if (!yaml.includes('line_item_to_product') || !yaml.includes('line_items.product_id') || !yaml.includes('products.id')) {
    console.error('Relationship not found or incorrect');
    process.exit(1);
}
console.log('Success');
INNER_EOF

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/inconvo-app with inconvo.yaml and index.js.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
