require('dotenv').config();
const fs = require('fs');
const Inconvo = require('@inconvoai/node');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  // Create a new conversation
  const conversation = await client.agents.conversations.create(agentId, {
    userIdentifier: '123',
  });

  const conversationId = conversation.id;

  // Send a message and receive the response
  const response = await client.agents.conversations.response.create(
    conversationId,
    {
      agentId: agentId,
      message: 'What are my top products?',
    }
  );

  // Save the response to response.json
  fs.writeFileSync(
    'response.json',
    JSON.stringify(response, null, 2),
    'utf-8'
  );

  console.log('Response saved to response.json');
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
