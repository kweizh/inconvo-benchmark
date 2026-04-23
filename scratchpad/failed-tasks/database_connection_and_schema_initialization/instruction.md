Inconvo requires introspecting the database to build its semantic model before any querying can happen. This establishes the baseline for the agent to understand available tables and data structures.

You need to use the Inconvo CLI to connect to a target PostgreSQL database, sync the schema, and pull the configuration files locally into the `.inconvo/` directory. 

**Constraints:**
- Must use the `npx inconvo connection sync` and `npx inconvo model pull` commands.
- The connection must securely use the `DATABASE_URL` environment variable.
- Do NOT manually create the `.inconvo/` directory; rely on the CLI tool.