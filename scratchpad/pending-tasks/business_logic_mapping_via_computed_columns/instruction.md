Often, users ask for metrics that do not exist as direct columns in the database but can be derived from existing data. Inconvo supports computed columns to define these virtual fields natively in the semantic layer.

You need to add a computed column named `is_active` to the `users` table configuration in the semantic model. This column should evaluate to true based on the SQL expression `last_login > '2025-01-01'`.

**Constraints:**
- The column must be defined entirely within the Inconvo semantic model configuration.
- The expression must strictly use the provided SQL date-comparison logic.
- Do not create a new view or modify the underlying PostgreSQL schema.