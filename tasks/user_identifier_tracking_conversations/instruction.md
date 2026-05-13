# Track Conversations per End-User with `userIdentifier`

## Background
Inconvo associates every conversation with an end-user via the `userIdentifier` parameter on `client.agents.conversations.create`. This is distinct from `userContext`, which scopes data access (for example, `organisationId`). `userIdentifier` is a stable per-end-user string used for analytics and persistence so that you can later list or retrieve conversations belonging to a specific end-user.

You must write a Node.js script that drives the `@inconvoai/node` SDK to create one conversation per end-user and persist the mapping between each `userIdentifier` and its returned conversation id.

## Requirements
- Read the list of end-user identifiers from the file `/home/user/inconvo-app/users.json`. The file contains the JSON array `["alice-001", "bob-002"]`.
- For each user identifier, in order:
  1. Create a conversation by calling `client.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: <id>, userContext: { organisationId: 1 } })`.
  2. Send the message `"Hello, what is my latest order amount?"` by calling `client.agents.conversations.response.create(conversation.id, { agentId: process.env.INCONVO_AGENT_ID, message: "Hello, what is my latest order amount?", stream: false })`.
  3. Write the response as JSON to `/home/user/inconvo-app/responses/<id>.json`.
- After both calls finish, write `/home/user/inconvo-app/conversation_ids.json` containing a JSON object that maps each `userIdentifier` to the conversation id returned for that user. For example: `{"alice-001": "<conv-id-alice>", "bob-002": "<conv-id-bob>"}`.

## Implementation Guide
1. Work inside `/home/user/inconvo-app`. The project is already initialised and `@inconvoai/node` and `dotenv` are already installed.
2. Create `index.js`:
   - `import "dotenv/config";`
   - `import Inconvo from "@inconvoai/node";`
   - `import fs from "node:fs";`
   - Read and parse `/home/user/inconvo-app/users.json`.
   - Instantiate `const client = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });`.
   - Ensure the `/home/user/inconvo-app/responses` directory exists.
   - Iterate over the user ids sequentially. For each id:
     - Call `client.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: id, userContext: { organisationId: 1 } })`.
     - Call `client.agents.conversations.response.create(conversation.id, { agentId: process.env.INCONVO_AGENT_ID, message: "Hello, what is my latest order amount?", stream: false })`.
     - Write the response object as pretty-printed JSON to `/home/user/inconvo-app/responses/${id}.json`.
     - Record the mapping from `id` to `conversation.id`.
   - After the loop, write the mapping as JSON to `/home/user/inconvo-app/conversation_ids.json`.
3. Run the script with `node index.js`.

## Constraints
- Project path: /home/user/inconvo-app
- Input file (already present): /home/user/inconvo-app/users.json
- Output files (must be produced): /home/user/inconvo-app/responses/alice-001.json, /home/user/inconvo-app/responses/bob-002.json, /home/user/inconvo-app/conversation_ids.json
- Use the real Inconvo Cloud API with the `INCONVO_API_KEY` and `INCONVO_AGENT_ID` environment variables.
- `userIdentifier` must be the per-end-user value from `users.json`. `userContext` must remain `{ organisationId: 1 }` for every call.
- Do NOT mock the SDK or stub network calls.

## Integrations
- Inconvo Cloud (requires INCONVO_API_KEY, INCONVO_AGENT_ID, INCONVO_DB_URL).