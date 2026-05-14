require('dotenv').config();
const fs = require('fs');
const Inconvo = require('@inconvoai/node').default || require('@inconvoai/node');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    const agentId = process.env.INCONVO_AGENT_ID;

    // 1. Create a conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123',
      userContext: { organisationId: 1 }
    });

    // 2. Send a message
    const response = await client.agents.conversations.response.create(
      conversation.id,
      {
        agentId: agentId,
        message: "What is the status of order 123?"
      }
    );

    // Save the raw JSON response
    fs.writeFileSync('/home/user/inconvo-bot/response.json', JSON.stringify(response, null, 2));
    console.log('Response saved to response.json');
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
