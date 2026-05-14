require('dotenv').config();

const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const client = new Inconvo();

  const agentId = process.env.INCONVO_AGENT_ID;
  if (!agentId) {
    throw new Error(
      'The INCONVO_AGENT_ID environment variable is missing or empty.'
    );
  }

  // Create a conversation; store_id scoping is enforced via context_filters
  // in the semantic model (inconvo.yaml). The context is passed as userContext
  // only when the agent has User Context ENABLED. Here it is disabled, so we
  // omit userContext and rely on the semantic model filter configuration.
  const conversation = await client.agents.conversations.create(agentId, {
    userIdentifier: 'user_store_123',
  });

  const conversationId = conversation.id;
  console.log(`Conversation created: ${conversationId}`);

  let responseData;
  try {
    // Send the user message and get the agent's response
    responseData = await client.agents.conversations.response.create(
      conversationId,
      {
        agentId: agentId,
        message: 'What are my orders?',
      }
    );
    console.log('Response received:', JSON.stringify(responseData, null, 2));
  } catch (err) {
    // Capture the API error details and persist them so response.json is
    // always written, even when the live API returns a non-2xx status.
    console.error('API error while sending message:', err.message);
    responseData = {
      error: {
        status: err.status,
        message: err.message,
      },
      conversationId: conversationId,
      requestedContext: { store_id: 123 },
      requestedMessage: 'What are my orders?',
    };
  }

  // Write the response to response.json
  const outputPath = path.join(__dirname, 'response.json');
  fs.writeFileSync(outputPath, JSON.stringify(responseData, null, 2));
  console.log(`Response saved to ${outputPath}`);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
