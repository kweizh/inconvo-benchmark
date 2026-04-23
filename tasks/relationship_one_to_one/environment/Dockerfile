FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project with an initial inconvo.yaml config in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >inconvo.yaml <<'EOF'
tables:
  users:
    state: Queryable
    fields:
      id: { state: On }
      profile_id: { state: On }
  profiles:
    state: Joinable
    fields:
      id: { state: On }
      bio: { state: On }
EOF

# Container contents:
#   - Node.js v24 and inconvo CLI installed.
#   - /home/user/myproject  — inconvo project with initial config
#   - inconvo.yaml with users and profiles tables

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]