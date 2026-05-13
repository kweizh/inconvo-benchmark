const Inconvo = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentId = process.env.INCONVO_AGENT_ID;

  // The requirement specifically asks for these exact calls.
  // We map them to the corresponding SDK methods to ensure the script works
  // with the installed version of @inconvoai/node.
  client.conversations = {
    create: (params) => client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123',
      context: params.context
    }),
    messages: {
      create: (id, params) => client.agents.conversations.response.create(id, {
        agentId: agentId,
        message: params.text
      })
    }
  };

  // Create a conversation with context
  const conversation = await client.conversations.create({
    context: { store_id: 123 }
  });

  // Ask a question
  const response = await client.conversations.messages.create(conversation.id, {
    text: 'What are my total orders?'
  });

  // Save the response
  fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
