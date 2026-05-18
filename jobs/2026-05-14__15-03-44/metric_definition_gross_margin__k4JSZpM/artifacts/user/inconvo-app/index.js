require('dotenv').config();
const Inconvo = require('@inconvoai/node');

// Initialize the Inconvo client
const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY
});

async function queryGrossMargin() {
  try {
    // Create a new conversation
    const conversation = await inconvo.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {
        userIdentifier: 'user_123'
      }
    );

    console.log('Conversation created:', conversation.id);

    // Send the query message
    const response = await inconvo.agents.conversations.response.create(
      conversation.id,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message: 'What is the average gross margin per month?',
        stream: false
      }
    );

    console.log('Response received:', JSON.stringify(response, null, 2));

    // Write the response to response.json
    const fs = require('fs');
    fs.writeFileSync(
      '/home/user/inconvo-app/response.json',
      JSON.stringify(response, null, 2)
    );

    console.log('Response saved to /home/user/inconvo-app/response.json');
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

queryGrossMargin();