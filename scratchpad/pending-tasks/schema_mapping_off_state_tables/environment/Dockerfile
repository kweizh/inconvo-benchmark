FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml exposing passwords."

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    cat >inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On }
      name: { state: On }
  passwords:
    state: Queryable
    fields:
      id: { state: On }
      hash: { state: On }
EOF

# Container contents:
#   - Node.js v24 and inconvo CLI installed.
#   - /home/user/app with inconvo.yaml

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]