require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  try {
    // Start a conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: '123',
    });

    // Send the message
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "What are my top products?",
    });

    // Save the response
    fs.writeFileSync('response.json', JSON.stringify(response, null, 2));
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
