# Customer Support Bot Order Status

## Background
You are building a customer support bot using Inconvo. Support agents need to be able to look up order statuses using natural language. You need to create a Node.js script that uses the `@inconvoai/node` SDK to query the order status.

## Requirements
- Initialize a Node.js project in `/home/user/inconvo-bot`.
- Install `@inconvoai/node` and `dotenv`.
- A `.env` file is already provided in the project directory with `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and `DATABASE_URL`.
- Create a semantic model `inconvo.yaml` that defines an `orders` table. The table should be `Queryable` and have fields: `id` (state: On), `status` (state: On, type: dimension), and `created_at` (state: On, type: dimension).
- Create a script `index.js` that initializes the Inconvo client and uses the Conversations API to send the message: "What is the status of order 123?".
- The script must save the raw JSON response from the Inconvo API to `/home/user/inconvo-bot/response.json`.

## Implementation Guide
1. `cd /home/user/inconvo-bot`
2. Run `npm init -y` to initialize the project.
3. Run `npm install @inconvoai/node dotenv` to install the dependencies.
4. Create `inconvo.yaml` with the required semantic model.
5. Create `index.js` which loads environment variables, initializes the Inconvo client, creates a conversation, sends the message "What is the status of order 123?", and writes the response to `response.json`.
6. Run `node index.js` to execute the script and generate the response.

## Constraints
- Project path: `/home/user/inconvo-bot`
- Log file: `/home/user/inconvo-bot/response.json`