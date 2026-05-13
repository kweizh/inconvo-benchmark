FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN npm i -g inconvo

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project environment with Node.js v24 and PostgreSQL client."

RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    cat >inconvo.yaml <<'EOF'
tables:
  yearly_metrics:
    state: Queryable
    fields:
      id: { state: On, type: dimension }
      year: { state: On, type: dimension }
      revenue_current: { state: On, type: measure }
      revenue_previous: { state: On, type: measure }
relations: []
EOF

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
