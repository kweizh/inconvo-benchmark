require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

// Initialize Inconvo client
const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

async function main() {
  try {
    const agentId = process.env.INCONVO_AGENT_ID;
    console.log('Creating conversation...');
    
    // Create a conversation
    const conversation = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: 'test_user',
    });
    console.log('Conversation created:', conversation.id);
    
    // Send the message
    const message = "What is the status of order 123?";
    console.log('Sending message:', message);
    
    const response = await inconvo.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: message,
    });
    
    console.log('Response received');
    
    // Save the raw JSON response to response.json
    const responsePath = '/home/user/inconvo-bot/response.json';
    fs.writeFileSync(responsePath, JSON.stringify(response, null, 2));
    console.log('Response saved to:', responsePath);
    
  } catch (error) {
    console.error('Error:', error);
    
    // Save the error response to response.json
    const responsePath = '/home/user/inconvo-bot/response.json';
    const errorResponse = {
      error: {
        message: error.message,
        status: error.status,
        headers: error.headers ? Object.fromEntries(error.headers) : undefined,
      }
    };
    fs.writeFileSync(responsePath, JSON.stringify(errorResponse, null, 2));
    console.log('Error response saved to:', responsePath);
    
    process.exit(1);
  }
}

main();