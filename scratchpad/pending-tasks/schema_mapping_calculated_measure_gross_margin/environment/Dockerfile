FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @inconvoai/node && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml containing an orders table with revenue and cost."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      revenue: { state: On, type: measure }
      cost: { state: On, type: measure }
EOF

# Container contents:
#   - Node.js v24 and @inconvoai/node installed
#   - /home/user/inconvo-app — project directory
#   - inconvo.yaml with orders table, revenue and cost fields

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
