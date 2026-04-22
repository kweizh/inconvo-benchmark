FROM node:20-slim

# Install PostgreSQL client for health checks or setup
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Initialize npm and install inconvo
RUN npm init -y && npm install inconvo

# Copy a script to initialize the database with some tables
COPY init_db.sql /app/init_db.sql

# We'll need a way to run the SQL against the database during setup
# DATABASE_URL will be provided at runtime
COPY setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh

# The user will run commands here
CMD ["/bin/bash"]
