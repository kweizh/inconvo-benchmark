In SaaS applications, multi-tenant databases require strict data isolation to ensure users from one organization cannot access data from another. Inconvo handles this via row-level security policies applied at runtime via user context.

You need to implement a security policy on the `sales` table configuration within the semantic model. This policy must automatically filter all generated queries by matching the `organisation_id` column to the `organisation_id` value passed in via `userContext`.

**Constraints:**
- The filtering policy must be applied at the semantic model level, not hardcoded into the application's backend.
- The policy must strictly expect `organisation_id` as the context key.
- Must ensure that any query on the `sales` table fails or returns empty if the `organisation_id` context is missing.