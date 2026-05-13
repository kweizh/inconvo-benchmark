const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  const client = new Inconvo();
  const agentId = process.env.INCONVO_AGENT_ID;
  
  if (!agentId) {
    console.error('INCONVO_AGENT_ID environment variable is not set');
    process.exit(1);
  }

  try {
    console.log('Creating conversation...');
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'test_user_123',
      userContext: { store_id: 123 }
    });

    console.log('Sending message...');
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "What are my orders?"
    });

    fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
