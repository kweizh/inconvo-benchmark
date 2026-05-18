require('dotenv').config();
const Inconvo = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

// Initialize Inconvo client
const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

async function main() {
  try {
    // Configuration
    const agentId = process.env.INCONVO_AGENT_ID || 'default-agent-id';
    const userIdentifier = 'user_123';
    const storeId = 123;

    console.log('Creating conversation with context...');
    
    // Create conversation with context { store_id: 123 }
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: userIdentifier,
      userContext: {
        store_id: storeId,
      },
    });

    console.log(`Conversation created with ID: ${conversation.id}`);

    console.log('Sending message: "What are my total orders?"');

    // Send message to the conversation
    const response = await client.agents.conversations.response.create(
      conversation.id,
      {
        agentId: agentId,
        message: 'What are my total orders?',
      }
    );

    console.log('Response received:', response);

    // Save response to JSON file
    const responsePath = path.join(__dirname, 'response.json');
    fs.writeFileSync(responsePath, JSON.stringify(response, null, 2), 'utf8');

    console.log(`Response saved to ${responsePath}`);
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();