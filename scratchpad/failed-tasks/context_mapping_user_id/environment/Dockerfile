FROM node:20-slim

# Install PostgreSQL client and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install inconvo CLI
RUN npm install -g inconvo@latest

# Set up python environment for tests
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install pytest psycopg2-binary pyyaml

WORKDIR /workspace

# Copy initial project files
COPY . .

# Initialize inconvo project structure if not present
# (In a real scenario, we might pre-generate these in the setup script)
RUN if [ ! -f inconvo.yaml ]; then \
    echo "tables:\n  sales:\n    state: Queryable\n    fields:\n      id: { state: On }\n      amount: { state: On, type: measure }\n      organisation_id: { state: On, type: dimension }" > inconvo.yaml; \
    fi

# The task expects DATABASE_URL to be provided at runtime
ENV DATABASE_URL=""

CMD ["/bin/bash"]
