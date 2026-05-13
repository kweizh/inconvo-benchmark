# Inconvo Express.js Endpoint

## Background
Inconvo provides an SDK for interacting with your Data Agents. You need to build a simple Express.js endpoint that uses the `@inconvoai/node` SDK to forward user questions to the Inconvo dev server.

## Requirements
- Initialize a Node.js project in `/home/user/inconvo-express`.
- Install `express` and `@inconvoai/node`.
- Create an `index.js` that sets up an Express server.
- Implement a POST `/ask` endpoint that accepts JSON body `{"question": "...", "userId": "..."}`.
- The endpoint must use the `INCONVO_API_KEY` and `INCONVO_AGENT_ID` environment variables.
- It should use the SDK to create a conversation for the given `userId` (using `userIdentifier`), and then send the `question` as a message to that conversation.
- Return the response from the message creation.

## Implementation Guide
1. `mkdir -p /home/user/inconvo-express && cd /home/user/inconvo-express`
2. `npm init -y`
3. `npm install express @inconvoai/node`
4. Create `index.js` and set up the Express app to parse JSON bodies.
5. Initialize the `Inconvo` client from `@inconvoai/node`.
6. In the POST `/ask` route, create a conversation using `client.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: req.body.userId })`.
7. Send the message using `client.agents.conversations.messages.create(process.env.INCONVO_AGENT_ID, conversation.id, { message: req.body.question })` (or equivalent SDK method based on the Inconvo SDK structure).
8. Start the server on the specified port.

## Constraints
- Project path: `/home/user/inconvo-express`
- Start command: `node index.js`
- Port: `3000`
- The server must read `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment.