require('dotenv/config');
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  try {
    // Initialize the Inconvo client with API key
    const inconvo = new Inconvo({
      apiKey: process.env.INCONVO_API_KEY
    });

    // Create a new conversation
    const userIdentifier = 'user-1';
    const conversation = await inconvo.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {
        userIdentifier
      }
    );

    // Write conversation id to file
    const convId = conversation.id;
    fs.writeFileSync('conversation_id.txt', convId);
    console.log('Conversation created with ID:', convId);

    // Send first message
    const firstResponse = await inconvo.agents.conversations.response.create(
      convId,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message: 'Show me my top 5 customers by total order amount.',
        stream: false
      }
    );

    // Write first response to JSON file
    fs.writeFileSync('first_response.json', JSON.stringify(firstResponse, null, 2));
    console.log('First response written to first_response.json');

    // Send followup message on the same conversation
    const secondResponse = await inconvo.agents.conversations.response.create(
      convId,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message: 'Now show me only those located in the United States.',
        stream: false
      }
    );

    // Write second response to JSON file
    fs.writeFileSync('second_response.json', JSON.stringify(secondResponse, null, 2));
    console.log('Second response written to second_response.json');

    console.log('All artifacts created successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();