import 'dotenv/config';
import Inconvo from '@inconvoai/node';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const tools = inconvoDataAgent({
    inconvo,
    agentId: process.env.INCONVO_AGENT_ID,
    userIdentifier: 'agent-user',
    userContext: {
      dbUrl: process.env.INCONVO_DB_URL,
    },
  });

  const { text } = await generateText({
    model: openai('gpt-4o'),
    tools,
    prompt: 'What is the total amount of orders? Please provide the final answer in plain text.',
    maxSteps: 10,
  });

  fs.writeFileSync(
    path.join(__dirname, 'response.json'),
    JSON.stringify({ response: text }, null, 2)
  );
  
  console.log(text);
}

main().catch(console.error);
