import 'dotenv/config';
import fs from 'fs';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { Inconvo } from '@inconvoai/node';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';

async function main() {
  const inconvoClient = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const tools = inconvoDataAgent({
    inconvo: inconvoClient,
    agentId: process.env.INCONVO_AGENT_ID,
    userIdentifier: 'user-123',
    userContext: { store_id: 1 }
  });

  try {
    const { text } = await generateText({
      model: openai('gpt-4o'),
      tools: tools,
      maxSteps: 10,
      prompt: 'What is the total amount of orders?',
    });

    const result = { response: text };
    fs.writeFileSync('/home/user/inconvo-agent/response.json', JSON.stringify(result, null, 2));
    console.log('Agent response saved to response.json');
  } catch (error) {
    console.error('Error running agent:', error);
    process.exit(1);
  }
}

main();
