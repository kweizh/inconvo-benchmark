require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.INCONVO_API_KEY;
  const agentId = process.env.INCONVO_AGENT_ID;

  if (!apiKey || !agentId) {
    console.error('Missing INCONVO_API_KEY or INCONVO_AGENT_ID in environment variables');
    process.exit(1);
  }

  const inconvo = new Inconvo({
    apiKey: apiKey,
  });

  try {
    // Create a new conversation
    // Providing store_id in userContext as requested by the API error
    const conversation = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: "pochi-user",
      userContext: { store_id: 1 }
    });

    // Send the message and get a response
    // Corrected property: inconvo.agents.conversations.response.create
    const response = await inconvo.agents.conversations.response.create(
      conversation.id,
      {
        agentId: agentId,
        message: "What is the average gross margin per month?",
        stream: false,
      }
    );

    // Save the response to response.json
    const outputPath = path.join(__dirname, 'response.json');
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    console.log(`Response saved to ${outputPath}`);
  } catch (error) {
    console.error('Error querying Inconvo:', error);
    process.exit(1);
  }
}

main();
