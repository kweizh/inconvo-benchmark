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
LABEL Description="Inconvo semantic model with tables defined but missing many-to-many relationships."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >inconvo.yaml <<'EOF'
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
  products:
    state: Queryable
    fields:
      id: { state: On }
      name: { state: On }
  line_items:
    state: Joinable
    fields:
      order_id: { state: On }
      product_id: { state: On }
relations: []
EOF

# Container contents:
#   - Node.js v24 and Inconvo CLI installed globally.
#   - /home/user/myproject - project directory.
#   - inconvo.yaml with orders, products, and line_items tables, and an empty relations array.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]