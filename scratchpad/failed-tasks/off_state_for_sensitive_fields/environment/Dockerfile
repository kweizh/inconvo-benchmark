FROM node:20-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment for tests
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install pytest psycopg2-binary PyYAML

# Install inconvo CLI
RUN npm install -g inconvo@latest

WORKDIR /app

# The DATABASE_URL will be provided at runtime
ENV DATABASE_URL=""

# Copy setup scripts if any (in this case we'll assume the DB is already populated or we provide a script)
COPY environment/setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh

# Default command
CMD ["/bin/bash"]
