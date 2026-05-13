# Inconvo Multi-tenant Reporting

## Background
Inconvo is an open-source platform for building "chat-with-data" agents. When building multi-tenant analytics, it's crucial to scope data so users can only query their own records. You can do this by implementing context filters in the semantic model.

## Requirements
- Configure the `inconvo.yaml` semantic model to include an `orders` table.
- Implement a context filter on the `orders` table that restricts queries to a specific `store_id` passed in the conversation context.
- Write a Node.js script (`index.js`) using the `@inconvoai/node` SDK to start a conversation with `context: { store_id: 123 }` and ask "What are my orders?".
- Save the API response to `response.json`.

## Implementation Guide
1. A Node.js project is already initialized at `/home/user/inconvo-app` with dependencies installed.
2. Edit `/home/user/inconvo-app/inconvo.yaml` to define the `orders` table and add the context filter for `store_id`.
3. Create `/home/user/inconvo-app/index.js` to initialize the Inconvo client (it will automatically pick up `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment).
4. In `index.js`, use `client.conversations.create({ context: { store_id: 123 } })` and `client.conversations.messages.create(...)` to ask "What are my orders?".
5. Write the final response data to `/home/user/inconvo-app/response.json`.
6. Run `node index.js` to generate the response.

## Constraints
- Project path: `/home/user/inconvo-app`
- The script must read credentials from environment variables.
- Output file: `/home/user/inconvo-app/response.json`