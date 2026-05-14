require("dotenv").config();
const fs = require("fs");
const Inconvo = require("@inconvoai/node");

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  // Start a conversation
  const conversation = await client.agents.conversations.create(agentId, {
    userIdentifier: "123",
  });

  // Send the message and receive the response
  const response = await client.agents.conversations.response.create(
    conversation.id,
    {
      agentId: agentId,
      message: "What are my top products?",
    }
  );

  fs.writeFileSync(
    "/home/user/inconvo-app/response.json",
    JSON.stringify(response, null, 2)
  );

  console.log("Response saved to response.json");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
