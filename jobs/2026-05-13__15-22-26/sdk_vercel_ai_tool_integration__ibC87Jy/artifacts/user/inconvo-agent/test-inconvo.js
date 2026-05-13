import 'dotenv/config';
import Inconvo from '@inconvoai/node';

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  try {
    const summary = await inconvo.agents.dataSummary.retrieve(process.env.INCONVO_AGENT_ID);
    console.log('Summary:', JSON.stringify(summary, null, 2));
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
