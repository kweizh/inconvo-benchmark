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
LABEL Description="Inconvo project with an initial inconvo.yaml missing relationship definitions."

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
      buyer_id: { state: On, type: dimension }
      seller_id: { state: On, type: dimension }
      total_amount: { state: On, type: measure }
  users:
    state: Joinable
    fields:
      id: { state: On }
      name: { state: On }
EOF

# Container contents:
#   - Node.js v24 installed
#   - /home/user/inconvo-app  — Inconvo project with initial config
#   - inconvo.yaml with orders and users tables but no relations

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
