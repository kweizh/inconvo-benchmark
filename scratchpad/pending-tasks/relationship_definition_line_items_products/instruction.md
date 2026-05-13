# Define a Many-to-One Relationship Between Line Items and Products

## Background
Inconvo uses a semantic model defined in `inconvo.yaml` to map natural language to data. Defining `relations` between tables enables Inconvo to traverse join paths when answering analytical questions. You have an existing Inconvo project at `/home/user/inconvo-app` whose semantic model already declares two tables (`line_items` and `products`) but does NOT yet declare any relations between them. Without the join, Inconvo cannot answer product-centric questions that aggregate over line items, such as "What is the most popular product name?".

You must update the semantic model to:
  - Mark `line_items` as `Queryable` (the table that gets queried).
  - Mark `products` as `Joinable` (it is only reachable via a join from `line_items`).
  - Add a `relations` entry named `line_item_to_product` that joins `line_items.product_id` to `products.id`.

Then update the existing `index.js` so that it uses the `@inconvoai/node` SDK to ask the Data Agent "What is the most popular product name?" and writes the raw agent response as JSON to `/home/user/inconvo-app/response.json`.

## Requirements
- Edit `/home/user/inconvo-app/inconvo.yaml` so that:
  - `tables.line_items.state` is `Queryable` with fields `id`, `order_id`, `product_id`, `quantity` (each with `state: On`).
  - `tables.products.state` is `Joinable` with fields `id`, `name`, `price` (each with `state: On`).
  - A top-level `relations` list contains an entry with `name: line_item_to_product`, `left: line_items.product_id`, `right: products.id`.
- Edit `/home/user/inconvo-app/index.js` so that it:
  - Loads environment variables from the process environment (`INCONVO_API_KEY`, `INCONVO_AGENT_ID`).
  - Imports `Inconvo` from `@inconvoai/node`.
  - Creates a conversation with the agent and sends the message: `What is the most popular product name?`.
  - Writes the raw JSON agent response to `/home/user/inconvo-app/response.json`.
- Run `node index.js` once so that the response file is produced.

## Implementation Guide
1. `cd /home/user/inconvo-app`
2. Update `inconvo.yaml`:
   - Confirm `line_items` has `state: Queryable` and its fields are listed.
   - Change `products` to `state: Joinable`.
   - Append a `relations` section that defines `line_item_to_product` joining `line_items.product_id` to `products.id`.
3. Edit `index.js` to send the question `What is the most popular product name?` to the agent and save the raw response to `response.json`.
4. Run `node index.js`.

## Constraints
- Project path: /home/user/inconvo-app
- Log file: /home/user/inconvo-app/response.json
- The `@inconvoai/node` SDK is already installed in `node_modules`.
- You MUST use the real `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `INCONVO_DB_URL` environment variables that are already present in the environment. Do NOT mock the SDK.

## Integrations
- Inconvo Cloud (via `@inconvoai/node` SDK)
