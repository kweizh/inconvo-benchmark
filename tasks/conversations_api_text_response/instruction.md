# Handle simple text response from the Conversations API

## Background
Inconvo provides a Conversations API to interact with your data agent programmatically. You need to create a simple Node.js script that sends a message to the agent and saves the response.

## Requirements
- Initialize a Node.js project in `/home/user/inconvo-app`.
- Install `@inconvoai/node` and `dotenv`.
- Create a script `index.js` that initializes the Inconvo client, creates a new conversation, and sends the message "What are my top products?" to the API.
- Save the response to `response.json` in the project directory.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/inconvo-app`.
2. Install the required dependencies: `npm install @inconvoai/node dotenv`.
3. Create `index.js`:
   - Load environment variables using `dotenv`.
   - Initialize the Inconvo client using `INCONVO_API_KEY` and `INCONVO_AGENT_ID`.
   - Call `client.conversations.create({ context: { user_id: 123 } })` to start a conversation.
   - Call `client.conversations.messages.create(id, { message: "What are my top products?" })`.
   - Save the returned response to `response.json` using `fs.writeFileSync`.
4. Run the script to generate `response.json`.

## Constraints
- Project path: `/home/user/inconvo-app`
- Log file: `/home/user/inconvo-app/response.json`
- The environment will have `INCONVO_API_KEY` and `INCONVO_AGENT_ID` set.

## Integrations
- None