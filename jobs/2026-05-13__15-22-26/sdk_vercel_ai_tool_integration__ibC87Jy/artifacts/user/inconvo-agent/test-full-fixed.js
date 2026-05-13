import 'dotenv/config';
import Inconvo from '@inconvoai/node';

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    console.log('Starting conversation...');
    const conversation = await inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
      userIdentifier: 'test-user'
    });
    console.log('Conversation:', JSON.stringify(conversation, null, 2));

    if (!conversation.id) {
        throw new Error('No conversation ID returned');
    }

    console.log('Messaging agent...');
    const response = await inconvo.agents.conversations.response.create(conversation.id, {
      agentId: process.env.INCONVO_AGENT_ID,
      message: 'What is the total amount of orders?'
    });
    console.log('Response:', JSON.stringify(response, null, 2));
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
