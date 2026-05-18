require('dotenv').config();
const Inconvo = require('@inconvoai/node');

async function main() {
  try {
    // Initialize the Inconvo client (automatically picks up INCONVO_API_KEY from environment)
    const client = new Inconvo({
      apiKey: process.env.INCONVO_API_KEY,
    });

    const agentId = process.env.INCONVO_AGENT_ID;

    console.log('Creating conversation with userContext: { store_id: 123 }');
    
    // Create a conversation with userContext containing store_id
    // Note: This requires User Context to be ENABLED for the agent
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123',
      userContext: {
        store_id: 123
      }
    });

    console.log('Conversation created:', conversation.id);

    // Ask "What are my orders?"
    console.log('Sending message: "What are my orders?"');
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "What are my orders?"
    });

    console.log('Response received');

    // Save the response to response.json
    const fs = require('fs');
    fs.writeFileSync('response.json', JSON.stringify(response, null, 2), 'utf8');
    
    console.log('Response saved to response.json');
    console.log('Response:', JSON.stringify(response, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
    if (error.response) {
      console.error('Response data:', JSON.stringify(error.response.data, null, 2));
    }
    process.exit(1);
  }
}

main();