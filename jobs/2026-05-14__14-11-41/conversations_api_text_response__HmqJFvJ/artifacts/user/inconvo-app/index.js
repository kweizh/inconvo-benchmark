require('dotenv').config();
const fs = require('fs');
const { Inconvo } = require('@inconvoai/node');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  try {
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123',
      userContext: { user_id: 123, organisationId: 1 }
    });
    
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "What are my top products?"
    });
    
    fs.writeFileSync('response.json', JSON.stringify(response, null, 2));
    console.log('Successfully saved to response.json');
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
