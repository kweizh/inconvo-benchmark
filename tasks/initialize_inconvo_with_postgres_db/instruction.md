# Initialize Inconvo Project with PostgreSQL

## Background
Inconvo requires a database connection to introspect the schema and generate the semantic model. Your task is to initialize a new Inconvo project and configure it to connect to an existing PostgreSQL database.

## Requirements
- You must initialize an Inconvo project in `/home/user/myproject`.
- You must configure the database connection by creating a `.env` file in the project directory.
- The `.env` file must contain the `DATABASE_URL` environment variable set to `postgresql://inconvo:inconvo@localhost:5432/inconvo_db`.
- The project must have a valid `inconvo.yaml` file after initialization.

## Implementation Guide
1. Navigate to `/home/user/myproject`.
2. Create a `.env` file and set `DATABASE_URL=postgresql://inconvo:inconvo@localhost:5432/inconvo_db`.
3. Run the appropriate command to initialize the Inconvo project (e.g., `npx inconvo@latest init` or the equivalent if it's a manual initialization).

## Constraints
- Project path: `/home/user/myproject`
- Database URL: `postgresql://inconvo:inconvo@localhost:5432/inconvo_db`