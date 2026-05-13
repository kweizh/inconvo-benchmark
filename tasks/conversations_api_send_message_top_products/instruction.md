# Inconvo Conversations API: Send Message

## Background
You need to use the `@inconvoai/node` SDK to interact with an Inconvo Data Agent. Your goal is to start a conversation, send a specific question, and parse the response.

## Requirements
- Initialize a Node.js project in `/home/user/inconvo-app`.
- Install `@inconvoai/node` and `dotenv`.
- Write a script `index.js` that uses the SDK to start a conversation and send the message "What are my top products?".
- Save the resulting JSON response to `/home/user/inconvo-app/response.json`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/inconvo-app`.
2. Install the required dependencies: `npm i @inconvoai/node dotenv`.
3. Create `index.js`.
4. In `index.js`, initialize the Inconvo client using the environment variables `INCONVO_API_KEY` and `INCONVO_AGENT_ID`.
5. Start a conversation using `client.conversations.create({ context: { user_id: 123 } })`.
6. Send the message using `client.conversations.messages.create(conversation.id, { message: "What are my top products?" })`.
7. Write the entire response object to `/home/user/inconvo-app/response.json` using `fs.writeFileSync`.

## Constraints
- Project path: /home/user/inconvo-app
- Output file: /home/user/inconvo-app/response.json
- The script must read `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment.

## Integrations
- None