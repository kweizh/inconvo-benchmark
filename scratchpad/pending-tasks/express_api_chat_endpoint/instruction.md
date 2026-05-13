# Express API Chat Endpoint with Inconvo

## Background
Inconvo is a platform for building chat-with-data agents. A common backend integration pattern is to expose a thin HTTP endpoint that forwards user questions from a client (web/mobile) to the Inconvo Data Agent and returns the structured response. In this task you will build a small Express.js application that proxies user messages to the Inconvo agent using the `@inconvoai/node` SDK.

## Requirements
- Build an Express.js HTTP server in the existing project at `/home/user/inconvo-app`.
- Expose a single `POST /chat` route that accepts a JSON body of the form `{ "message": string, "userId": string }`.
- The route must validate that the `message` field is present and non-empty. If it is missing/empty, respond with HTTP `400` and a JSON body `{ "error": "message is required" }`.
- The route must:
  1. Initialize an Inconvo client using `process.env.INCONVO_API_KEY`.
  2. Call `inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: userId, userContext: { organisationId: 1 } })` to start a new agent conversation.
  3. Call `inconvo.agents.conversations.response.create(conversation.id, { agentId: process.env.INCONVO_AGENT_ID, message, stream: false })` to obtain the agent response.
  4. Send the response object returned by Inconvo back to the client as JSON (HTTP 200).
- The server MUST listen on port `3001`.
- The application entry file MUST be `/home/user/inconvo-app/index.js`. Running `node index.js` from `/home/user/inconvo-app` starts the server.
- Use the existing `@inconvoai/node`, `dotenv`, and `express` packages already installed in `/home/user/inconvo-app/node_modules`. Do NOT mock any dependency.

## Implementation Guide
1. Open `/home/user/inconvo-app/index.js` and use CommonJS `require` to import `express` and `@inconvoai/node`.
2. Create an Express app, configure it with `express.json()` so JSON request bodies are parsed.
3. Implement the `POST /chat` route described in the Requirements section.
4. Read `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment (do not hardcode any values).
5. Start the server with `app.listen(3001)`.

## Constraints
- Project path: /home/user/inconvo-app
- Entry file: /home/user/inconvo-app/index.js
- Start command: node index.js
- Port: 3001
- Required env vars: INCONVO_API_KEY, INCONVO_AGENT_ID, INCONVO_DB_URL
- Do NOT mock the Inconvo SDK or any HTTP calls. The endpoint must hit the real Inconvo service.

## Integrations
- Inconvo (via @inconvoai/node)
