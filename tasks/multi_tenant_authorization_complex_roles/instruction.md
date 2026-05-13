# Multi-tenant Authorization with Complex Roles

## Background
You are building a multi-tenant analytics dashboard using Inconvo. You have two types of users: `admin` and `store_manager`. Admins can see all orders across all stores, while store managers can only see orders for their specific `store_id`. You need to configure the semantic model and write a Node.js script to dynamically apply context filters based on the user's role.

## Requirements
- Create a semantic model `inconvo.yaml` that defines an `orders` table with a `store_id` column.
- Write a Node.js script `index.js` that uses the `@inconvoai/node` SDK to create a conversation.
- The script should export a function `askQuestion(query, user)` where `user` is an object like `{ role: 'store_manager', store_id: 123 }` or `{ role: 'admin' }`.
- The script must correctly pass context filters to `client.conversations.create({ context: ... })` so that `store_manager` users are restricted to their `store_id`, but `admin` users are not restricted.
- The script must send the `query` using `client.conversations.messages.create` and return the response text.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/inconvo-app`.
2. Install `@inconvoai/node` and `dotenv`.
3. Create `inconvo.yaml` defining the `orders` table (make sure it's `Queryable` and has `store_id` as a dimension).
4. Create `index.js` exporting the `askQuestion` function.
5. The `askQuestion` function should initialize the Inconvo client using `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment.
6. Construct the `context` object appropriately based on `user.role`.

## Constraints
- Project path: `/home/user/inconvo-app`
- The script `index.js` must be a CommonJS module exporting `askQuestion`.
- You do not need to start a server, just provide the `index.js` file with the correct logic.