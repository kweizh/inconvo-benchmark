const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
require('dotenv').config();

const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});
const agentId = process.env.INCONVO_AGENT_ID;

async function main() {
  try {
    const conversation = await client.agents.conversations.create(agentId, { userIdentifier: 'user_123', userContext: { user_id: 123, organisationId: 1 } });
    const response = await client.agents.conversations.response.create(conversation.id, { agentId, message: "What are my top products?" });
    fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
    console.log("Success");
  } catch (error) {
    console.error("Error:", error);
  }
}

main();
