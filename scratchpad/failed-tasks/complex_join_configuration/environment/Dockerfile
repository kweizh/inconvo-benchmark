FROM ubuntu:24.04

# Install basic dependencies and PostgreSQL client
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Inconvo CLI
RUN npm install -g @inconvoai/cli

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project environment with PostgreSQL client and Node.js v24."

# Set up the project directory and initial state
# Note: DATABASE_URL must be provided at runtime for real PostgreSQL
# We'll create the directory and a mock .inconvo setup that would be there after 'inconvo model pull'
# But since we want the agent to run 'inconvo model pull', we'll just set up the directory and a dummy package.json
RUN mkdir -p /home/user/inconvo-project && \
    cd /home/user/inconvo-project && \
    npm init -y && \
    npm install @inconvoai/node

# We need to simulate the state where an agent exists but the relation is missing.
# In a real Harbor task, DATABASE_URL would point to a real DB.
# For the sake of the Dockerfile, we'll just ensure the directory is ready.

# Container contents:
#   - Inconvo CLI installed
#   - Node.js v24 and PostgreSQL client
#   - /home/user/inconvo-project: project directory with @inconvoai/node installed

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
