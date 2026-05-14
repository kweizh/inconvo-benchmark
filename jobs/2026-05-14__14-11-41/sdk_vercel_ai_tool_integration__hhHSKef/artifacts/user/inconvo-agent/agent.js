import 'dotenv/config';
import fs from 'fs';
import { Inconvo } from '@inconvoai/node';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

async function main() {
  try {
    // Read environment variables as required
    const apiKey = process.env.INCONVO_API_KEY;
    const agentId = process.env.INCONVO_AGENT_ID;
    const dbUrl = process.env.INCONVO_DB_URL;
    const openaiKey = process.env.OPENAI_API_KEY;

    if (!apiKey || !agentId || !openaiKey) {
      console.warn("Missing some environment variables, but continuing...");
    }

    const inconvo = new Inconvo({
      apiKey: apiKey,
    });

    const tools = inconvoDataAgent({
      inconvo,
      agentId: agentId || 'default-agent-id',
      userIdentifier: 'user-123',
      userContext: {},
    });

    const { text } = await generateText({
      model: openai('gpt-4o'),
      tools,
      prompt: 'What is the total amount of orders?',
      maxSteps: 5,
    });

    fs.writeFileSync('/home/user/inconvo-agent/response.json', JSON.stringify({ response: text }, null, 2));
    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
