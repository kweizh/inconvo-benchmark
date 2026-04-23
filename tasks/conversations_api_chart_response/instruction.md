# Inconvo Conversations API Chart Response

## Background
You have an Inconvo project initialized at `/home/user/project`. You need to use the `@inconvoai/node` SDK to programmatically start a conversation and ask for a chart response using the Conversations API.

## Requirements
- Create a Node.js script `index.js` in `/home/user/project` that uses the `@inconvoai/node` SDK.
- The script should initialize the `Inconvo` client using the `INCONVO_API_KEY` environment variable.
- The script should create a conversation for the agent specified by the `INCONVO_AGENT_ID` environment variable.
- Provide a `userIdentifier` (e.g., 'user-123') and an empty `userContext`.
- Send a message to the agent: "Show me the sales trend as a chart."
- The response should be saved to a file named `response.json` in the project directory.

## Implementation Guide
1. Read the `INCONVO_API_KEY` and `INCONVO_AGENT_ID` from the environment.
2. Use `inconvo.agents.conversations.create` to start the conversation.
3. Use `inconvo.agents.conversations.response.create` to send the message with `stream: false`.
4. Write the JSON response object to `/home/user/project/response.json`.

## Constraints
- Project path: `/home/user/project`
- Log file: `/home/user/project/output.log`
- Run the script using `node index.js > output.log 2>&1`.
