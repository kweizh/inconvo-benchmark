import 'dotenv/config';
import Inconvo from '@inconvoai/node';

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    const agent = await inconvo.get(`/agents/${process.env.INCONVO_AGENT_ID}`);
    console.log('Agent:', JSON.stringify(agent, null, 2));
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
