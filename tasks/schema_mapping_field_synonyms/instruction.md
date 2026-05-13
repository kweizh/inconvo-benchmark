# Add Field Synonyms to the Inconvo Semantic Model

## Background
Inconvo's semantic layer maps natural language to your database schema using `inconvo.yaml`. Synonyms allow you to teach the agent alternative business terms that users may use when asking questions (for example, "revenue" instead of "total_amount").

A pre-existing Inconvo project lives at `/home/user/inconvo-app`. It already contains:
- An installed `node_modules` directory with `@inconvoai/node` and `dotenv`.
- A starter `inconvo.yaml` that defines an `orders` table (Queryable) and a `customers` table (Joinable) with a relation from `orders.customer_id` to `customers.id`.
- A `package.json` for the project.

The environment variables `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL` are already exported into the container's process environment, so `process.env.INCONVO_API_KEY` and `process.env.INCONVO_AGENT_ID` can be read directly from Node.

No synonyms have been configured yet.

## Requirements
1. Edit `/home/user/inconvo-app/inconvo.yaml` to add synonyms:
   - On the `total_amount` field of the `orders` table, add the synonyms `["revenue", "sales", "income"]`.
   - On the `name` field of the `customers` table, add the synonyms `["customer", "buyer", "client"]`.
2. Write (or edit) `/home/user/inconvo-app/index.js` so that when executed with `node index.js`:
   - It loads environment variables from `.env` using `dotenv`.
   - It uses the `@inconvoai/node` SDK to create a conversation against the agent identified by `INCONVO_AGENT_ID`.
   - It sends the natural language message `"What is the total revenue per buyer?"` and waits for a non-streaming response.
   - It writes the raw JSON response from the Inconvo API to `/home/user/inconvo-app/response.json`.
3. Run `node index.js` so that `response.json` is produced.

## Implementation Guide
1. `cd /home/user/inconvo-app`
2. Open `inconvo.yaml` and add a `synonyms` key under the `total_amount` and `name` fields. The exact YAML you use must keep the existing structure intact. For example:
   ```yaml
   tables:
     orders:
       state: Queryable
       fields:
         id: { state: On }
         total_amount:
           state: On
           type: measure
           synonyms: ["revenue", "sales", "income"]
         created_at: { state: On, type: dimension }
     customers:
       state: Joinable
       fields:
         id: { state: On }
         name:
           state: On
           synonyms: ["customer", "buyer", "client"]
   relations:
     - name: order_to_customer
       left: orders.customer_id
       right: customers.id
   ```
3. Create `index.js` similar to the snippet below, using the real environment variables `INCONVO_API_KEY` and `INCONVO_AGENT_ID`:
   ```javascript
   import "dotenv/config";
   import { randomUUID } from "node:crypto";
   import fs from "node:fs";
   import Inconvo from "@inconvoai/node";

   const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

   async function main() {
     const convo = await inconvo.agents.conversations.create(
       process.env.INCONVO_AGENT_ID,
       { userIdentifier: randomUUID().toString() }
     );
     const response = await inconvo.agents.conversations.response.create(
       convo.id,
       {
         agentId: process.env.INCONVO_AGENT_ID,
         message: "What is the total revenue per buyer?",
         stream: false,
       }
     );
     fs.writeFileSync("response.json", JSON.stringify(response, null, 2));
   }

   main().catch((err) => {
     console.error(err);
     process.exit(1);
   });
   ```
   You may use either ESM (`import`) or CommonJS (`require`) syntax — the project's `package.json` supports both because `@inconvoai/node` ships with dual exports.
4. Run the script:
   ```bash
   node index.js
   ```
5. Confirm that `/home/user/inconvo-app/response.json` was written.

## Constraints
- Project path: `/home/user/inconvo-app`
- Log file: `/home/user/inconvo-app/response.json`
- Do NOT delete or rename the existing `orders` or `customers` table definitions or the existing relation.
- Do NOT mock the Inconvo SDK; the script must actually call the live Inconvo API using the real credentials.
- The `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL` environment variables are already exported into the container's process environment.

## Integrations
- Inconvo Cloud (uses `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, `INCONVO_DB_URL`).