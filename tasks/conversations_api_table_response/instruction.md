# Inconvo Conversations API Table Response

## Background
Inconvo is an open-source platform for building reliable "chat-with-data" agents. It uses a Semantic Layer to map natural language into structured queries. The Conversations API allows programmatic interaction with the agent.

## Requirements
- Initialize an Inconvo project.
- Create a semantic model `inconvo.yaml` for an e-commerce database with `orders` and `products`.
- Write a Node.js script that uses the `@inconvoai/node` SDK to start a conversation and send a natural language query.
- The script should ask "What are my top products?" and log the table response to a JSON file.

## Implementation Guide
1. Create a project directory at `/home/user/inconvo-app`.
2. Initialize a default `package.json` and install `inconvo` and `@inconvoai/node`.
3. Create `inconvo.yaml` defining `orders` (with `total_amount` measure) and `products` (with `name` dimension) and a relation between them.
4. Create `index.js` that initializes the `@inconvoai/node` client, creates a conversation, sends the message "What are my top products?", and writes the resulting table data to `/home/user/inconvo-app/response.json`.

## Constraints
- Project path: `/home/user/inconvo-app`
- Log file: `/home/user/inconvo-app/response.json`

## Integrations
- None