FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-yaml bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo semantic model task environment"

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat > inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On }
      customer_name: { state: On, type: dimension }
EOF

# Container contents:
#   - Node.js v24 and inconvo CLI installed
#   - /home/user/myproject with initial inconvo.yaml

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]