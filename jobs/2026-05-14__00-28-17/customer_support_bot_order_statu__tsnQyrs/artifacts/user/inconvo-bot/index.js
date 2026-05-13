const Inconvo = require('@inconvoai/node');
const fs = require('fs');
require('dotenv').config();

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    // Create a conversation
    const conversation = await client.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
      userIdentifier: 'user_123',
      userContext: { store_id: 1 }, // Added required store_id
    });

    // Send the message
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: process.env.INCONVO_AGENT_ID,
      message: 'What is the status of order 123?',
    });

    // Save the raw JSON response
    fs.writeFileSync('/home/user/inconvo-bot/response.json', JSON.stringify(response, null, 2));
    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
