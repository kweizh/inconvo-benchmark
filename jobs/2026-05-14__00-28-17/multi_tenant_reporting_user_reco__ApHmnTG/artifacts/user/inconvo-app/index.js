const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  const client = new Inconvo();
  const agentId = process.env.INCONVO_AGENT_ID;

  // Polyfill to match the prompt's suggested API structure
  // and map 'context' to 'userContext' as required by the SDK/API
  client.conversations = {
    create: (params) => {
      const { context, ...rest } = params;
      return client.agents.conversations.create(agentId, {
        userIdentifier: 'user_123',
        userContext: context, // Map context to userContext
        ...rest
      });
    },
    messages: {
      create: (conversationId, params) => client.agents.conversations.response.create(conversationId, {
        agentId: agentId,
        ...params
      })
    }
  };

  try {
    console.log("Creating conversation...");
    const conversation = await client.conversations.create({
      context: { store_id: 123 }
    });
    
    console.log("Sending message...");
    const response = await client.conversations.messages.create(conversation.id, {
      message: "What are my orders?"
    });
    
    fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
    console.log("Response saved to response.json");
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

main();
