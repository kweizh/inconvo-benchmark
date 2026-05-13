import 'dotenv/config';
import { Inconvo } from '@inconvoai/node';

async function test() {
  const inconvoClient = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    const conversation = await inconvoClient.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
      userIdentifier: 'user-123',
      userContext: { store_id: 1 }
    });
    console.log('Conversation created:', conversation.id);
  } catch (error) {
    console.error('Error creating conversation:', error);
  }
}

test();
