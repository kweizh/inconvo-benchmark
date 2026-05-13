# Inconvo Conversations API: Multi-turn Followup

## Background
Inconvo's Conversations API supports multi-turn conversations where the Data Agent retains context across messages within the same conversation. This allows users to ask a question, then refine the request with a followup that depends on the previous turn's context (e.g. "now show me only those in the United States").

You will use the `@inconvoai/node` SDK to start a conversation, send an initial analytical question, and then send a contextual followup on the SAME conversation id.

## Requirements
- A Node.js project is already initialized at `/home/user/inconvo-app` with `@inconvoai/node` and `dotenv` installed (see `package.json` and `node_modules`). A `.env` file is present that references `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL`.
- Create a script `/home/user/inconvo-app/index.js` that:
  1. Loads environment variables via `dotenv/config`.
  2. Initializes the Inconvo client with `INCONVO_API_KEY`.
  3. Creates a new conversation against `INCONVO_AGENT_ID` with `userContext: { organisationId: 1 }`.
  4. Writes the conversation id to `/home/user/inconvo-app/conversation_id.txt`.
  5. Sends the FIRST message on that conversation: `"Show me my top 5 customers by total order amount."` (non-streaming) and writes the full JSON response to `/home/user/inconvo-app/first_response.json`.
  6. Sends a FOLLOWUP message on the SAME conversation id: `"Now show me only those located in the United States."` (non-streaming) and writes the full JSON response to `/home/user/inconvo-app/second_response.json`.
- The script must exit with code 0.

## Implementation Guide
1. `cd /home/user/inconvo-app`.
2. Inspect the existing `package.json`, `.env`, and `node_modules` — do not reinitialize the project.
3. Create `index.js` using ES module or CommonJS as preferred; the SDK supports both.
4. Use `inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier, userContext: { organisationId: 1 } })` to start the conversation.
5. Use `inconvo.agents.conversations.response.create(convId, { agentId: process.env.INCONVO_AGENT_ID, message: "...", stream: false })` twice with the SAME `convId` to send the first message and the followup.
6. Persist all three artifacts (`conversation_id.txt`, `first_response.json`, `second_response.json`) using `fs.writeFileSync`.
7. Run `node index.js` to produce the artifacts.

## Constraints
- Project path: `/home/user/inconvo-app`
- Output files: `/home/user/inconvo-app/conversation_id.txt`, `/home/user/inconvo-app/first_response.json`, `/home/user/inconvo-app/second_response.json`
- Both messages MUST be sent on the same conversation id (multi-turn).
- Use real `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL` from the environment — do NOT hardcode or mock.

## Integrations
- None