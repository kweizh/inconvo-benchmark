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
LABEL Description="Node.js v24 environment with a pre-initialized Inconvo + Express project at /home/user/inconvo-app."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    cat >package.json <<'EOF'
{
  "name": "inconvo-express-chat",
  "version": "1.0.0",
  "private": true,
  "description": "Express endpoint that proxies user messages to the Inconvo Data Agent.",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "@inconvoai/node": "^0.8.0",
    "dotenv": "^16.4.5",
    "express": "^4.19.2"
  }
}
EOF

RUN cd /home/user/inconvo-app && \
    npm install --no-audit --no-fund && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
      created_at: { state: On, type: dimension }
  products:
    state: Queryable
    fields:
      id: { state: On }
      name: { state: On }
relations:
  - name: order_to_product
    left: orders.product_id
    right: products.id
EOF

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the Express + Inconvo task environment
#   - /home/user/inconvo-app: pre-initialized Node.js project with package.json declaring
#       express, @inconvoai/node, and dotenv as dependencies. node_modules is pre-installed.
#   - /home/user/inconvo-app/inconvo.yaml: starter semantic model file

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
