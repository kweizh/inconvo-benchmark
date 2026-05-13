# Define a `gross_margin` Calculated Measure with Inconvo

## Background
Inconvo's Semantic Model (`inconvo.yaml`) lets you define calculated measures directly on a table. Calculated measures are derived from other fields and can then be queried in natural language. You will add a new `gross_margin` measure to the `orders` table, derived from `total_amount` and `cost`, and then ask the Data Agent for the average gross margin per month.

## Requirements
- You have an existing Node.js project at `/home/user/inconvo-app` with `@inconvoai/node` and `dotenv` already installed.
- A starter `inconvo.yaml` is already present in the project directory. It defines `orders` (as `Queryable`) and `customers` (as `Joinable`), but it does NOT yet contain a `gross_margin` measure.
- A `.env` file is already present referencing `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL`. Do NOT modify it.
- Edit `inconvo.yaml` to add a calculated measure named `gross_margin` to the `orders` table. Its `type` must be `measure` and its formula must reference both `total_amount` and `cost` using the `-` operator (i.e. `total_amount - cost`).
- Write `index.js` in the project root which:
  1. Loads environment variables with `dotenv`.
  2. Initializes the Inconvo client from `@inconvoai/node` using `process.env.INCONVO_API_KEY`.
  3. Creates a new conversation against `process.env.INCONVO_AGENT_ID` using `inconvo.agents.conversations.create`.
  4. Calls `inconvo.agents.conversations.response.create` with the message `"What is the average gross margin per month?"` and `stream: false`.
  5. Writes the resulting JSON response to `/home/user/inconvo-app/response.json` using `JSON.stringify`.
- Run `node index.js` so `response.json` is created with real data returned from the Inconvo Cloud agent.

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml` and locate the existing `orders` table block.
2. Under `orders.fields`, add an entry similar to:
   ```yaml
   gross_margin:
     state: On
     type: measure
     formula: total_amount - cost
   ```
   Use whichever exact key (`formula`, `expression`, `sql`, etc.) is appropriate for your semantic model as long as the field is a `measure` and the expression contains both `total_amount` and `cost` with a `-` operator.
3. Create `/home/user/inconvo-app/index.js` that uses `@inconvoai/node` to send the natural language query and save the JSON response.
4. Run the script: `node index.js`.

## Constraints
- Project path: `/home/user/inconvo-app`
- Log file: `/home/user/inconvo-app/response.json`
- Do NOT hardcode API keys, agent IDs, or database URLs anywhere in source. Always read them from `process.env`.
- Do NOT mock the Inconvo SDK; the script must hit the real Inconvo Cloud API.

## Integrations
- Inconvo Cloud (`INCONVO_API_KEY`, `INCONVO_AGENT_ID`)
- PostgreSQL (`INCONVO_DB_URL`)