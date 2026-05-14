'use strict';

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const Inconvo = require('@inconvoai/node').default;

const AGENT_ID = process.env.INCONVO_AGENT_ID;

if (!AGENT_ID) {
  console.error('Error: INCONVO_AGENT_ID environment variable is not set.');
  process.exit(1);
}

const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

// Convenience wrapper that mirrors the required API surface:
//   client.conversations.create({ context })
//   client.conversations.messages.create(conversationId, { message })
const conversations = {
  /**
   * Create a new conversation with the given context (mapped to userContext).
   * @param {{ context: Record<string, string|number|boolean> }} params
   * @returns {Promise<{ id: string }>}
   */
  create: ({ context }) =>
    client.agents.conversations.create(AGENT_ID, {
      userIdentifier: 'user_default',
      userContext: context,
    }),

  messages: {
    /**
     * Send a message within an existing conversation and receive a response.
     * @param {string} conversationId
     * @param {{ message: string }} params
     * @returns {Promise<import('@inconvoai/node').Agents.ResponseCreateResponse>}
     */
    create: (conversationId, { message }) =>
      client.agents.conversations.response.create(conversationId, {
        agentId: AGENT_ID,
        message,
      }),
  },
};

async function main() {
  // 1. Create a conversation with store_id context for multi-tenant filtering.
  const conversation = await conversations.create({ context: { store_id: 123 } });
  console.log('Conversation created:', conversation.id);

  // 2. Ask the question inside that conversation.
  const response = await conversations.messages.create(conversation.id, {
    message: 'What are my total orders?',
  });
  console.log('Response received:', response.message ?? response);

  // 3. Persist the full JSON response to response.json.
  const outputPath = path.join(__dirname, 'response.json');
  fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
  console.log(`Response written to ${outputPath}`);
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
