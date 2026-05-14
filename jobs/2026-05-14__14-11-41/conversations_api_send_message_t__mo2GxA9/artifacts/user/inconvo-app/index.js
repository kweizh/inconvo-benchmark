require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
  // Initialize the Inconvo client using the environment variables INCONVO_API_KEY and INCONVO_AGENT_ID
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
    agentId: process.env.INCONVO_AGENT_ID
  });
  
  const agentId = process.env.INCONVO_AGENT_ID;

  // Polyfill to support the prompt's requested SDK structure against the actual SDK structure
  if (!client.conversations) {
    client.conversations = {
      create: async ({ context }) => {
        return await client.agents.conversations.create(agentId, {
          userIdentifier: 'user_' + context.user_id,
          userContext: { ...context, organisationId: 1 }
        });
      },
      messages: {
        create: async (conversationId, { message }) => {
          return await client.agents.conversations.response.create(conversationId, {
            agentId,
            message
          });
        }
      }
    };
  }

  try {
    // Start a conversation
    const conversation = await client.conversations.create({ context: { user_id: 123 } });

    // Send the message
    const response = await client.conversations.messages.create(conversation.id, { message: "What are my top products?" });

    // Write the entire response object to /home/user/inconvo-app/response.json
    fs.writeFileSync('/home/user/inconvo-app/response.json', JSON.stringify(response, null, 2));
    console.log("Successfully wrote response to response.json");
  } catch (error) {
    console.error("Error:", error);
  }
}

main();
