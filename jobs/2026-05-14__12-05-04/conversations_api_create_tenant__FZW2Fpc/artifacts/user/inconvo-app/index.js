require('dotenv').config({ override: true });
const { Inconvo } = require('@inconvoai/node');
const { randomUUID } = require('crypto');
const fs = require('fs');

async function main() {
  const apiKey = process.env.INCONVO_API_KEY;
  const agentId = process.env.INCONVO_AGENT_ID;
  const outputPath = '/home/user/inconvo-app/output.json';

  const client = new Inconvo({
    apiKey: apiKey,
  });

  try {
    // Create a conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: randomUUID().toString(),
      userContext: { organisationId: 2 },
    });

    // Send a query
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "QUERY",
    });

    // Save the response
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    console.log('Response saved to output.json');
  } catch (error) {
    // Save the error message
    fs.writeFileSync(outputPath, JSON.stringify({ error: error.message }, null, 2));
    console.error('Error occurred and saved to output.json:', error.message);
  }
}

main();
