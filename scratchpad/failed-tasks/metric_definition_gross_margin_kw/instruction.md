# Metric Definition: Gross Margin

## Background
Inconvo allows defining computed columns (calculated measures) directly in the semantic layer (`inconvo.yaml`). This enables the AI agent to answer questions about derived metrics that do not exist as physical columns in the database.

## Requirements
You need to add a calculated measure named `gross_margin` to the `orders` table in the Inconvo semantic model. The measure should calculate the gross margin as `revenue - cost`.

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Locate the `orders` table configuration.
3. Add a new field named `gross_margin` with the SQL expression `revenue - cost` and `type: measure`.

## Constraints
- Project path: /home/user/myproject
- The column must be defined entirely within the Inconvo semantic model configuration.
- Do not create a new view or modify the underlying PostgreSQL schema.
- The `DATABASE_URL` environment variable is required to run the evaluation.