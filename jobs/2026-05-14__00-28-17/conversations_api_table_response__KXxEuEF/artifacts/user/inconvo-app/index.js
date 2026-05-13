const Inconvo = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function run() {
  // Initialize the Inconvo client
  const client = new Inconvo({
    apiKey: process.env['INCONVO_API_KEY'] || 'YOUR_API_KEY',
  });

  const agentId = process.env['INCONVO_AGENT_ID'] || 'YOUR_AGENT_ID';

  try {
    console.log('Starting conversation...');
    
    // 1. Create a conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123',
    });

    console.log(`Created conversation: ${conversation.id}`);

    // 2. Send the natural language query "What are my top products?"
    console.log('Sending query: "What are my top products?"');
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: 'What are my top products?',
    });

    // 3. Check if the response is a table and log it to a JSON file
    if (response.type === 'table' && response.table) {
      const outputPath = '/home/user/inconvo-app/response.json';
      fs.writeFileSync(outputPath, JSON.stringify(response.table, null, 2));
      console.log(`Table response successfully saved to ${outputPath}`);
    } else if (response.type === 'text') {
      console.log('Received text response:', response.message);
    } else {
      console.log('Received response of type:', response.type);
    }
  } catch (error) {
    if (error instanceof Inconvo.APIError) {
      console.error(`API Error: ${error.status} - ${error.name}`);
      console.error(error.message);
    } else {
      console.error('An unexpected error occurred:', error);
    }
  }
}

run();
