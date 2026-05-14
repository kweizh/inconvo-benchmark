'use strict';

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { Inconvo } = require('@inconvoai/node');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  let rawResponse;

  try {
    // Step 1: Create a new conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'support-agent',
    });

    const conversationId = conversation.id;

    // Step 2: Send the message and receive a response
    rawResponse = await client.agents.conversations.response.create(conversationId, {
      agentId: agentId,
      message: 'What is the status of order 123?',
    });
  } catch (err) {
    // Capture the API error as the raw response
    rawResponse = {
      error: err.constructor.name,
      message: err.message,
      status: err.status,
    };
  }

  // Step 3: Write the raw JSON response to response.json
  const outputPath = path.join(__dirname, 'response.json');
  fs.writeFileSync(outputPath, JSON.stringify(rawResponse, null, 2));

  console.log('Response saved to response.json');
  console.log(JSON.stringify(rawResponse, null, 2));
}

main().catch((err) => {
  console.error('Unexpected error:', err);
  process.exit(1);
});
