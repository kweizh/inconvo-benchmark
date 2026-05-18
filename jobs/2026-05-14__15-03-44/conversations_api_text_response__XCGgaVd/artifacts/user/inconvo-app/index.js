require('dotenv').config();
const Inconvo = require('@inconvoai/node');
const fs = require('fs');

// Initialize the Inconvo client
const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY
});

async function main() {
  try {
    const agentId = process.env.INCONVO_AGENT_ID;
    
    // Create a new conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123'
    });
    
    console.log('Conversation created:', conversation.id);
    
    // Send a message to the conversation
    const response = await client.agents.conversations.response.create(
      conversation.id,
      { 
        agentId: agentId,
        message: "What are my top products?" 
      }
    );
    
    console.log('Response received:', response);
    
    // Save the response to response.json
    fs.writeFileSync(
      '/home/user/inconvo-app/response.json',
      JSON.stringify(response, null, 2)
    );
    
    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();