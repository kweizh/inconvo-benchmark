import 'dotenv/config';
import Inconvo from '@inconvoai/node';

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    console.log('Starting conversation with empty context...');
    const conversation = await inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
      userIdentifier: 'test-user',
      userContext: {}
    });
    console.log('Conversation:', JSON.stringify(conversation, null, 2));
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
