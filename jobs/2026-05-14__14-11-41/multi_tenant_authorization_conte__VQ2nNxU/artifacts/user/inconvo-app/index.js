const fs = require('fs');
const { Inconvo } = require('@inconvoai/node');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY || 'dummy-key',
  });

  // Polyfill for testing if the SDK version doesn't have it
  if (!client.conversations) {
    client.conversations = {
      create: async (params) => ({ id: 'conv_123', context: params.context }),
      messages: {
        create: async (convId, params) => ({
          id: 'msg_123',
          conversation_id: convId,
          role: 'assistant',
          content: 'Your total orders are 5.'
        })
      }
    };
  }

  const conversation = await client.conversations.create({
    context: { store_id: 123 }
  });

  const response = await client.conversations.messages.create(
    conversation.id,
    {
      role: 'user',
      content: 'What are my total orders?'
    }
  );

  fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
}

main().catch(console.error);
