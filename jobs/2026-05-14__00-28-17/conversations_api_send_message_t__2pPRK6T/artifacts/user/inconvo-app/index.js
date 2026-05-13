require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.INCONVO_API_KEY;
  const agentId = process.env.INCONVO_AGENT_ID;

  if (!apiKey || !agentId) {
    console.error('Error: INCONVO_API_KEY and INCONVO_AGENT_ID environment variables are required.');
    process.exit(1);
  }

  const client = new Inconvo({
    apiKey: apiKey,
    agentId: agentId,
  });

  try {
    // Start a conversation
    const conversation = await client.conversations.create({
      context: { user_id: 123 }
    });

    // Send the message
    const response = await client.conversations.messages.create(conversation.id, {
      message: "What are my top products?"
    });

    // Save the resulting JSON response to response.json
    const outputPath = path.join(__dirname, 'response.json');
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    console.log(`Successfully saved response to ${outputPath}`);
  } catch (error) {
    console.error('Error interacting with Inconvo API:', error.message);
    process.exit(1);
  }
}

main();
