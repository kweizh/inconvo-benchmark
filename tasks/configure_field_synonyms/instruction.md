# Configure Field Synonyms

## Background
Inconvo uses a Semantic Layer to map natural language questions into structured query plans. The semantic model defines how the agent interprets data, including measures, dimensions, and their synonyms. Your task is to add synonyms for the `customer_name` field in the `users` table so the agent can understand alternative terms.

## Requirements
- You have an existing Inconvo project located at `/home/user/myproject` with a semantic model defined in `inconvo.yaml`.
- The `users` table currently has a `customer_name` field.
- You must add `client` and `shopper` as synonyms for the `customer_name` field.

## Implementation Guide
1. Navigate to `/home/user/myproject`.
2. Open `inconvo.yaml` and locate the `users` table.
3. Under the `customer_name` field, add a `synonyms` array containing `client` and `shopper`.

## Constraints
- Project path: `/home/user/myproject`
- The file to edit is `/home/user/myproject/inconvo.yaml`.