require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

// Initialize the Inconvo client
const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
  agentId: process.env.INCONVO_AGENT_ID,
});

async function sendMessage() {
  try {
    // Start a conversation
    const conversation = await client.conversations.create({
      context: {
        user_id: 123,
      },
    });

    console.log('Conversation started with ID:', conversation.id);

    // Send the message
    const response = await client.conversations.messages.create(conversation.id, {
      message: 'What are my top products?',
    });

    console.log('Message sent successfully');

    // Write the response to response.json
    fs.writeFileSync(
      '/home/user/inconvo-app/response.json',
      JSON.stringify(response, null, 2)
    );

    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

sendMessage();