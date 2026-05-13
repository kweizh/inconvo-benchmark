# Create a Conversation with Tenant Context

## Background
Inconvo is a platform for building chat-with-data agents. You need to write a Node.js script that uses the `@inconvoai/node` SDK to programmatically start a new conversation with a specific tenant context.

## Requirements
- Initialize a Node.js project.
- Install `@inconvoai/node` and `dotenv`.
- Write a script `index.js` that initializes the Inconvo client using environment variables.
- Create a conversation using the client with the context `{"tenant_id": "tenant_456"}`.
- Save the resulting conversation object as JSON to `/home/user/inconvo-app/output.json`.

## Implementation Guide
1. Run `npm init -y` in `/home/user/inconvo-app`.
2. Install the required packages: `npm install @inconvoai/node dotenv`.
3. Create `.env` with dummy values for `INCONVO_API_KEY` and `INCONVO_AGENT_ID`.
4. In `index.js`, import `Inconvo` from `@inconvoai/node`.
5. Initialize the client and call `client.conversations.create({ context: { tenant_id: "tenant_456" } })`.
6. Catch any errors (since dummy keys are used) and write the error message or the response to `output.json`.

## Constraints
- Project path: /home/user/inconvo-app
- Log file: /home/user/inconvo-app/output.json

## Integrations
- None