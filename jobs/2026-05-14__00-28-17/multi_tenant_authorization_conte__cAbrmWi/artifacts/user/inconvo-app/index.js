const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  // Shim to support the required syntax as per requirements
  client.conversations = {
    create: (params) => {
      const { context, ...rest } = params;
      return client.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
        userIdentifier: 'user_123',
        userContext: context,
        ...rest
      });
    },
    messages: {
      create: (conversationId, params) => {
        const { text, ...rest } = params;
        return client.agents.conversations.response.create(conversationId, { 
          agentId: process.env.INCONVO_AGENT_ID, 
          message: text,
          ...rest 
        });
      }
    }
  };

  try {
    // Create a conversation with context
    const conversation = await client.conversations.create({
      context: { store_id: 123 },
    });

    // Ask the question
    const response = await client.conversations.messages.create(conversation.id, {
      text: 'What are my total orders?',
    });

    // Save the response to response.json
    const responsePath = path.join('/home/user/inconvo-app', 'response.json');
    fs.writeFileSync(responsePath, JSON.stringify(response, null, 2));
    
    console.log(`Response saved to ${responsePath}`);
  } catch (error) {
    console.error('Error executing Inconvo script:', error);
    process.exit(1);
  }
}

main();
