import "dotenv/config";
import Inconvo from "@inconvoai/node";
import fs from "node:fs";

// Read and parse the users.json file
const users = JSON.parse(fs.readFileSync("/home/user/inconvo-app/users.json", "utf8"));

// Instantiate the Inconvo client
const client = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

// Ensure the responses directory exists
if (!fs.existsSync("/home/user/inconvo-app/responses")) {
  fs.mkdirSync("/home/user/inconvo-app/responses", { recursive: true });
}

// Iterate over the user ids sequentially
const conversationIds = {};
for (const id of users) {
  // Create a conversation
  const conversation = await client.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {
      userIdentifier: id,
      userContext: { organisationId: 1 }
    }
  );

  // Send a message to the conversation
  const response = await client.agents.conversations.response.create(
    conversation.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "Hello, what is my latest order amount?",
      stream: false
    }
  );

  // Write the response as pretty-printed JSON
  fs.writeFileSync(
    `/home/user/inconvo-app/responses/${id}.json`,
    JSON.stringify(response, null, 2)
  );

  // Record the mapping from user id to conversation id
  conversationIds[id] = conversation.id;
}

// Write the mapping to conversation_ids.json
fs.writeFileSync(
  "/home/user/inconvo-app/conversation_ids.json",
  JSON.stringify(conversationIds, null, 2)
);