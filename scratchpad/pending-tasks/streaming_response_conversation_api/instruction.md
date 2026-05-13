# Stream a Data Agent Response with the Inconvo Node SDK

## Background
The Inconvo `@inconvoai/node` SDK supports streaming responses from a Data Agent via Server-Sent Events when `stream: true` is passed to `inconvo.agents.conversations.response.create(...)`. The SDK returns an async iterable that emits `response.created`, `response.progress`, and `response.completed` events. You need to write a Node.js script that consumes this stream end-to-end and records every event to disk along with a final summary of the streaming session.

## Requirements
- Use the existing Node.js project at `/home/user/inconvo-app`. `package.json` already lists `@inconvoai/node` and `dotenv` as dependencies, and `node_modules` is already installed (do NOT re-run `npm install`).
- Write `index.js` that:
  1. Loads environment variables with `dotenv` and reads `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment.
  2. Creates an Inconvo client and starts a conversation with `inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: "stream-user", userContext: { organisationId: 1 } })`.
  3. Calls `inconvo.agents.conversations.response.create(conv.id, { agentId: process.env.INCONVO_AGENT_ID, message: "Summarize our sales trends for the last 3 months", stream: true })` to obtain an async iterable stream.
  4. Iterates the stream with `for await (const chunk of stream)`, writing each chunk as a single JSON line (`JSON.stringify(chunk) + "\n"`) to `/home/user/inconvo-app/stream.jsonl`. The file must be created from scratch (truncated) at the start of the run.
  5. Tracks the total number of chunks received (`chunkCount`) and the final assistant message string. The final message must be extracted from the `response.completed` event (e.g. `event.response.message` for a text response, or `JSON.stringify(event.response)` otherwise) and must be a non-empty string.
  6. After the stream ends, writes `/home/user/inconvo-app/summary.json` containing `{ "chunkCount": <number>, "finalMessage": "<string>" }`.

## Implementation Guide
1. `cd /home/user/inconvo-app`.
2. Create `index.js` using `import Inconvo from "@inconvoai/node"` (ESM) or `const Inconvo = require("@inconvoai/node").default` (CJS) — `package.json` is already configured for ESM (`"type": "module"`).
3. Use `fs.createWriteStream` (or repeated `fs.appendFileSync` after truncating the file) to write one JSON object per line to `stream.jsonl`.
4. Increment a counter for each chunk and capture the final message from the `response.completed` event.
5. Run `node index.js` to verify the script executes end-to-end and produces both output files.

## Constraints
- Project path: /home/user/inconvo-app
- Log file: /home/user/inconvo-app/stream.jsonl
- Summary file: /home/user/inconvo-app/summary.json
- Required env vars (already injected into the environment): `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, `INCONVO_DB_URL`.
- Do not run `npm install` — the dependencies are already installed in `node_modules`.
- Must call the SDK with `stream: true` and iterate the returned async iterable. Do NOT make a non-streaming request and synthesize chunks.

## Integrations
- Inconvo Cloud Data Agent (configured via `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL`).
