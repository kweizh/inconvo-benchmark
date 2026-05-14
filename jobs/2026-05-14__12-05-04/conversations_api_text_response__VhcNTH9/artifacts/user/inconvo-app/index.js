const { Inconvo } = require('@inconvoai/node');
require('dotenv').config();
const fs = require('fs');

const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
  agentId: process.env.INCONVO_AGENT_ID,
});

const agentId = process.env.INCONVO_AGENT_ID;

async function main() {
  try {
    // Initialize a new conversation with the required context
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: '123',
      userContext: { 
        user_id: 123,
        organisationId: 123 // Required by the API for this agent
      },
    });

    // Send the message "What are my top products?"
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "What are my top products?",
    });

    // Save the response to response.json
    fs.writeFileSync('response.json', JSON.stringify(response, null, 2));
    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
