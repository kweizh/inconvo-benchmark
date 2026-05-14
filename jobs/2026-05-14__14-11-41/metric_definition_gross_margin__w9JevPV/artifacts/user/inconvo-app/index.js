require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  const conversation = await inconvo.agents.conversations.create(agentId, { 
    userIdentifier: 'user_123',
    userContext: { store_id: 1 }
  });

  const response = await inconvo.agents.conversations.response.create(
    conversation.id,
    {
      agentId: agentId,
      message: "What is the average gross margin per month?",
      stream: false
    }
  );

  fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
}

main().catch(console.error);
