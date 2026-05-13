require('dotenv').config();
const { InconvoClient } = require('@inconvoai/node');

const client = new InconvoClient({
  apiKey: process.env.INCONVO_API_KEY,
});

const AGENT_ID = process.env.INCONVO_AGENT_ID;

/**
 * Asks a question to the Inconvo agent with role-based context filters.
 * 
 * @param {string} query - The user's question.
 * @param {Object} user - The user object containing role and store_id.
 * @param {string} user.role - 'admin' or 'store_manager'.
 * @param {number} [user.store_id] - The store ID for store managers.
 * @returns {Promise<string>} - The response text from the agent.
 */
async function askQuestion(query, user) {
  const context = {};

  if (user.role === 'store_manager') {
    if (!user.store_id) {
      throw new Error('store_id is required for store_manager role');
    }
    // Apply context filter to restrict orders to the user's store_id
    context.filters = [
      {
        table: 'orders',
        column: 'store_id',
        operator: '=',
        value: user.store_id,
      },
    ];
  }

  // Create a conversation with the appropriate context
  const conversation = await client.conversations.create({
    agent_id: AGENT_ID,
    context: context,
  });

  // Send the query as a message
  const message = await client.conversations.messages.create(conversation.id, {
    text: query,
  });

  return message.text;
}

module.exports = {
  askQuestion,
};
