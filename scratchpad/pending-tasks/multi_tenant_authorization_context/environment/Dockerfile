FROM node:18

RUN apt-get update && apt-get install -y python3 python3-pip postgresql-client

RUN npm install -g inconvo@latest

WORKDIR /app

# The DATABASE_URL will be provided at runtime
ENV DATABASE_URL=""

# Copy task files if any (instruction.md will be provided by Harbor)
# COPY . .

CMD ["/bin/bash"]
