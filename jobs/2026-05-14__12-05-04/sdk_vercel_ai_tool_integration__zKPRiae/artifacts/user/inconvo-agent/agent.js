import { Inconvo } from '@inconvoai/node';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import dotenv from 'dotenv';
import fs from 'fs/promises';

dotenv.config();

// Ensure required environment variables are present
const {
  INCONVO_API_KEY,
  INCONVO_AGENT_ID,
  INCONVO_DB_URL,
  OPENAI_API_KEY
} = process.env;

if (!INCONVO_API_KEY || !INCONVO_AGENT_ID || !OPENAI_API_KEY) {
  console.error('Missing required environment variables');
  process.exit(1);
}

async function main() {
  try {
    const inconvo = new Inconvo({
      apiKey: INCONVO_API_KEY,
    });

    const tools = inconvoDataAgent({
      inconvo,
      agentId: INCONVO_AGENT_ID,
      userIdentifier: 'agent-user-1',
      userContext: {
        // Optional context for the query
      },
    });

    console.log('Asking agent: What is the total amount of orders?');

    const result = await generateText({
      model: openai('gpt-4o'),
      prompt: 'What is the total amount of orders?',
      tools,
      maxSteps: 5,
      onStepFinish: (step) => {
        console.log(`Step ${step.stepNumber} finished.`);
        if (step.toolCalls.length > 0) {
          console.log(`Tool calls: ${step.toolCalls.map(tc => tc.toolName).join(', ')}`);
        }
        if (step.toolResults.length > 0) {
          console.log(`Tool results: ${JSON.stringify(step.toolResults, null, 2)}`);
        }
      }
    });

    console.log('Agent response:', result.text);
    console.log('Tool calls:', JSON.stringify(result.toolCalls, null, 2));

    const output = {
      response: result.text
    };

    await fs.writeFile('/home/user/inconvo-agent/response.json', JSON.stringify(output, null, 2));
    console.log('Response saved to response.json');
  } catch (error) {
    console.error('Error running agent:', error);
    process.exit(1);
  }
}

main();
