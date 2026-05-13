# Multi-tenant Authorization with Inconvo

## Background
Inconvo allows mapping application-level user context to database-level tenant IDs. You need to implement a context filter on the `orders` table that restricts queries to a specific `store_id` passed in the conversation context.

## Requirements
- You have an existing Node.js project at `/home/user/inconvo-app` with `@inconvoai/node` installed.
- Update `inconvo.yaml` to include a context filter on the `orders` table for `store_id`.
- Write a Node.js script `index.js` that uses the Inconvo SDK to create a conversation with context `{ store_id: 123 }`, asks 'What are my total orders?', and saves the JSON response to `response.json`.

## Constraints
- Project path: `/home/user/inconvo-app`
- The script must use `client.conversations.create({ context: { store_id: 123 } })` and `client.conversations.messages.create(...)`.
- The script must write the response to `/home/user/inconvo-app/response.json`.

## Integrations
- Inconvo Cloud
- PostgreSQL