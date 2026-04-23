# Use a base image with Node.js and Python
FROM node:20-bookworm

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user
RUN useradd -m user
USER user
WORKDIR /home/user

# Install Inconvo CLI globally
USER root
RUN npm install -g inconvo@latest
USER user

# Install Python dependencies for tests
# Create a virtualenv for tests
RUN python3 -m venv /home/user/venv
ENV PATH="/home/user/venv/bin:$PATH"
RUN pip install pytest psycopg2-binary pyyaml

# The database setup will be handled by the Harbor environment (using DATABASE_URL)
# But we need to ensure the schema is initialized.
# We'll use a script to initialize the DB if it's empty.
COPY --chown=user:user environment/init_db.sql /home/user/init_db.sql

# We'll run this script as part of the entrypoint or in the task setup if needed
# For Harbor, the Dockerfile should just prepare the environment.

CMD ["/bin/bash"]
