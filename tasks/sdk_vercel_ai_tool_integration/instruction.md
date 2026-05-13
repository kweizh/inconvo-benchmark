# Inconvo Vercel AI SDK Tool Integration

## Background
You need to integrate Inconvo as a tool within a Vercel AI SDK agent workflow. The agent should be able to answer natural language questions by querying an e-commerce database through Inconvo's semantic layer.

## Requirements
- Initialize a Node.js project in `/home/user/inconvo-agent`.
- Install necessary dependencies: `@inconvoai/node`, `@inconvoai/vercel-ai-sdk`, `ai`, `@ai-sdk/openai`, and `dotenv`.
- Create an `inconvo.yaml` semantic model defining `orders` (Queryable) and `customers` (Joinable) tables, with a relationship from `orders.customer_id` to `customers.id`.
- Create an `agent.js` script that uses the Vercel AI SDK `generateText` function with an OpenAI model.
- Provide the Inconvo tool to the agent so it can answer questions about the data.
- The script should ask the agent: "What is the total amount of orders?" and save the agent's textual response to `/home/user/inconvo-agent/response.json` as a JSON object `{"response": "..."}`.

## Implementation Guide
1. `mkdir -p /home/user/inconvo-agent` and initialize the project.
2. Install the required packages.
3. Create `inconvo.yaml` based on standard Inconvo configuration for an e-commerce schema.
4. Create `agent.js` that initializes the Inconvo client, wraps it as a Vercel AI SDK tool using `@inconvoai/vercel-ai-sdk`, and calls `generateText`.
5. Write the output of `generateText` to `response.json`.

## Constraints
- Project path: `/home/user/inconvo-agent`
- Log file: `/home/user/inconvo-agent/output.log`
- The script must read `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, `INCONVO_DB_URL`, and `OPENAI_API_KEY` from the environment.
- Run the script and pipe output to the log file.

## Integrations
- OpenAI