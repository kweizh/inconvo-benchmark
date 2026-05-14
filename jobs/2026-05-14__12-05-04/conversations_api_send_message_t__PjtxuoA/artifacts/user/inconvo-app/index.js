require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function main() {
  // Initialize the Inconvo client using environment variables
  const apiKey = process.env.INCONVO_API_KEY;
  const agentId = process.env.INCONVO_AGENT_ID;

  if (!apiKey || !agentId) {
    console.error('Missing INCONVO_API_KEY or INCONVO_AGENT_ID in environment variables.');
    process.exit(1);
  }

  const client = new Inconvo({
    apiKey: apiKey,
  });

  try {
    // 5. Start a conversation
    // Note: In @inconvoai/node v0.8.0, the conversations resource is under client.agents.
    // We also include organisationId: 1 as it is required by the agent's context schema.
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: '123',
      userContext: { user_id: 123, organisationId: 1 }
    });

    // 6. Send the message "What are my top products?"
    // In this version of the SDK, responses are created via client.agents.conversations.response.
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "What are my top products?"
    });

    // 7. Write the entire response object to /home/user/inconvo-app/response.json
    const outputPath = path.join(__dirname, 'response.json');
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));

    console.log(`Response saved to ${outputPath}`);
  } catch (error) {
    console.error('Error interacting with Inconvo API:', error);
  }
}

main();
