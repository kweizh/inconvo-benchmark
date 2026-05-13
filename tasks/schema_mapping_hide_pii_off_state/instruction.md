# Hide PII Fields by Setting State to Off

## Background
Inconvo uses a semantic model defined in `inconvo.yaml` to map natural language questions to safe, validated SQL queries. To prevent sensitive PII (personally identifiable information) from being exposed to the agent, individual fields can be hidden by setting their `state` to `Off`. You have an existing Inconvo project at `/home/user/inconvo-app` where the `customers` table currently exposes the `email` and `phone` fields (both with `state: On`). Your job is to hide these PII fields and then call the Inconvo Data Agent from a Node.js script to confirm the agent still works for non-PII queries.

## Requirements
- Update `/home/user/inconvo-app/inconvo.yaml` so that the `email` and `phone` fields under the `customers` table have `state: Off`.
- Leave the remaining fields (e.g. `customers.id`, `customers.name`, and all `orders` fields) untouched with `state: On` so they remain queryable.
- Do not change the table-level `state: Queryable` for `customers` or `orders`.
- Create (or edit) `/home/user/inconvo-app/index.js` so that it uses the `@inconvoai/node` SDK to:
  - Read `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from environment variables (the SDK reads `INCONVO_API_KEY` from env automatically; `INCONVO_AGENT_ID` is the agent id you pass to `inconvo.agents.conversations.create`).
  - Start a new conversation via `inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: "user-pii-off-test" })`.
  - Send the natural language question `"List customer names and their total orders"` via `inconvo.agents.conversations.response.create(conversationId, { agentId: process.env.INCONVO_AGENT_ID, message: "List customer names and their total orders", stream: false })`.
  - Write the JSON-stringified response from the agent to `/home/user/inconvo-app/response.json`.
- Run `node index.js` from the project directory so that `response.json` is produced.

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml`.
2. Under `tables.customers.fields`, change `email: { state: On }` to `email: { state: Off }` and `phone: { state: On }` to `phone: { state: Off }`.
3. Write `/home/user/inconvo-app/index.js` using the snippet below as a starting point:

```javascript
import Inconvo from "@inconvoai/node";
import fs from "node:fs";

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
  const conversation = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    { userIdentifier: "user-pii-off-test" },
  );
  const response = await inconvo.agents.conversations.response.create(
    conversation.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "List customer names and their total orders",
      stream: false,
    },
  );
  fs.writeFileSync("response.json", JSON.stringify(response, null, 2));
}

main().catch((err) => { console.error(err); process.exit(1); });
```

4. From `/home/user/inconvo-app`, run `node index.js`.

## Constraints
- Project path: /home/user/inconvo-app
- Log file: /home/user/inconvo-app/response.json
- Use the `@inconvoai/node` SDK (already installed under `node_modules`). Do not introduce mocks.
- The script must read the `INCONVO_API_KEY` and `INCONVO_AGENT_ID` values from the environment; do not hardcode them.

## Integrations
- None