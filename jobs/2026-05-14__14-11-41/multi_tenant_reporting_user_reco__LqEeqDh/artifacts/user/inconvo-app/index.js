const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  const client = new Inconvo();
  const agentId = process.env.INCONVO_AGENT_ID;

  // Polyfill to match the exact syntax requested in the prompt
  client.conversations = {
    create: async (params) => {
      return await client.agents.conversations.create(agentId, {
        userIdentifier: "user_123",
        userContext: params.context
      });
    },
    messages: {
      create: async (conversationId, params) => {
        return await client.agents.conversations.response.create(conversationId, {
          agentId: agentId,
          message: params.content
        });
      }
    }
  };

  // Start a conversation with context
  const conversation = await client.conversations.create({ context: { store_id: 123 } });
  
  // Ask "What are my orders?"
  const message = await client.conversations.messages.create(conversation.id, {
    content: "What are my orders?"
  });

  // Save the API response
  fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(message, null, 2));
}

main().catch(console.error);
