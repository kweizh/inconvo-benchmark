Exposing raw database schemas can lead to data leaks if sensitive columns like passwords or internal system configurations are passed to the LLM context. The Inconvo semantic model allows explicit toggling of table and column visibility.

You need to modify the pulled Inconvo model configuration to hide sensitive fields. Specifically, locate the `users` table in the semantic model and set the `password_hash` and `secret_key` column states to `Off`.

**Constraints:**
- Only modify the configuration files located within the `.inconvo/` directory.
- Do NOT execute any `ALTER TABLE` or `DROP COLUMN` SQL statements on the actual database.
- The table state of `users` must remain `Queryable`.