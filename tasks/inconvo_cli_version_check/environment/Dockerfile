FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g inconvo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project && chmod 0755 /home/user /home/user/project

LABEL Author="any-task-builder"
LABEL Description="Environment with Inconvo CLI installed and a basic project directory."

# Container contents:
#   - Node.js v24 installed
#   - inconvo CLI installed globally via npm
#   - /home/user/project directory created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
