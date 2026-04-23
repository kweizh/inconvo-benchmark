# Configuring Synonyms for Fields in Inconvo Semantic Model

## Background
Inconvo uses a Semantic Layer to map natural language questions into structured query plans. To improve the accuracy of matching user queries to database columns, you can define synonyms for specific fields.

## Requirements
- You have an Inconvo project initialized in `/home/user/myproject`.
- The database schema has a `customers` table with a `full_name` column. The database URL is available in the `DATABASE_URL` environment variable.
- Create a `.env` file in `/home/user/myproject` with the `DATABASE_URL` variable.
- Update the semantic model (`inconvo.yaml`) to make the `full_name` field queryable and add synonyms "client name" and "purchaser" to it.

## Implementation
1. Open the existing `/home/user/myproject/inconvo.yaml` file.
2. Ensure the `customers` table is defined with `state: Queryable`.
3. Add the `full_name` field under `customers` fields.
4. Set its `state` to `On`, `type` to `dimension`, and add a `synonyms` array containing `"client name"` and `"purchaser"`.
5. Create a `.env` file in `/home/user/myproject` and write the `DATABASE_URL` to it.

## Constraints
- Project path: `/home/user/myproject`