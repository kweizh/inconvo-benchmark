# Metric Definition (Gross Margin)

## Background
Inconvo uses a Semantic Layer to map natural language questions into structured query plans. Often, users ask for metrics that do not exist as direct columns in the database but can be derived from existing data. Inconvo supports computed columns to define these virtual fields natively in the semantic layer.

## Requirements
You need to add a computed column named `gross_margin` to the `products` table configuration in the semantic model. This column should evaluate to the percentage profit margin based on the SQL expression `(price - cost) / price * 100`.

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Locate the `products` table configuration.
3. Add a new field named `gross_margin` with the SQL expression `(price - cost) / price * 100` and `type: measure`.
4. Set the `unit` of the `gross_margin` field to `%`.

## Constraints
- Project path: `/home/user/myproject`
- The column must be defined entirely within the Inconvo semantic model configuration.
- The expression must strictly use the provided SQL logic.
- Do not create a new view or modify the underlying PostgreSQL schema.
- The `DATABASE_URL` environment variable is required to run the evaluation.