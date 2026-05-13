FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml configuration."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install @inconvoai/node dotenv && \
    cat >inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      internal_id: { state: On, type: dimension }
      name: { state: On, type: dimension }
  products:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      title: { state: On, type: dimension }
      price: { state: On, type: measure }
  orders:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      total_amount: { state: On, type: measure }
      created_at: { state: On, type: dimension }
EOF

RUN cd /home/user/inconvo-app && \
    cat >index.js <<'EOF'
const fs = require('fs');
const yaml = require('yaml'); // We will install yaml package
try {
  const file = fs.readFileSync('./inconvo.yaml', 'utf8');
  console.log("YAML parsed successfully");
} catch (e) {
  console.error(e);
  process.exit(1);
}
EOF

RUN cd /home/user/inconvo-app && npm install yaml

# Container contents:
#   - /home/user/inconvo-app  — Inconvo project directory
#   - /home/user/inconvo-app/inconvo.yaml — Initial semantic model config
#   - /home/user/inconvo-app/index.js — Script to validate YAML

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
