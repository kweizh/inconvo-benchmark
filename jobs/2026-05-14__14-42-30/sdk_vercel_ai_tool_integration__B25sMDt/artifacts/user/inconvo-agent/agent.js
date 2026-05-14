import 'dotenv/config';
import { createOpenAI } from '@ai-sdk/openai';
import { generateText } from 'ai';
import Inconvo from '@inconvoai/node';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Validate required environment variables
const requiredEnvVars = [
  'INCONVO_API_KEY',
  'INCONVO_AGENT_ID',
  'INCONVO_DB_URL',
  'OPENAI_API_KEY',
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

// Initialise the Inconvo client (picks up INCONVO_API_KEY from env automatically)
const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

// Build the set of Vercel AI SDK-compatible Inconvo tools
const inconvoTools = inconvoDataAgent({
  name: '',               // no name prefix → tools are named generically
  inconvo,
  agentId: process.env.INCONVO_AGENT_ID,
  userIdentifier: 'agent-user',
  userContext: {
    db_url: process.env.INCONVO_DB_URL,
  },
});

// Initialise the OpenAI provider
const openai = createOpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function main() {
  console.log('Starting Inconvo agent…');

  const result = await generateText({
    model: openai('gpt-4o-mini'),
    tools: inconvoTools,
    maxSteps: 10,                   // allow multi-step tool calling
    system: [
      'You are a helpful data analyst assistant.',
      'Use the available Inconvo tools to answer questions about the e-commerce database.',
      'Always start by getting the data agent connected data summary before asking questions.',
      'Provide clear, concise answers based on the data returned by the tools.',
    ].join('\n'),
    prompt: 'What is the total amount of orders?',
  });

  // `result.text` holds the final assistant text when available.
  // As a fallback, walk the steps in reverse to find the last assistant text message.
  let agentResponse = result.text;

  if (!agentResponse) {
    for (let i = result.steps.length - 1; i >= 0; i--) {
      const step = result.steps[i];
      if (step.text) {
        agentResponse = step.text;
        break;
      }
      // Also check response messages for assistant content
      if (step.response?.messages) {
        for (let j = step.response.messages.length - 1; j >= 0; j--) {
          const msg = step.response.messages[j];
          if (msg.role === 'assistant') {
            const content = Array.isArray(msg.content)
              ? msg.content
                  .filter((c) => c.type === 'text')
                  .map((c) => c.text)
                  .join('')
              : String(msg.content ?? '');
            if (content) {
              agentResponse = content;
              break;
            }
          }
        }
      }
      if (agentResponse) break;
    }
  }

  if (!agentResponse) {
    // Summarise tool interactions as a best-effort response
    const toolCallSummaries = result.steps.flatMap((step) =>
      (step.toolCalls ?? []).map((tc) => `Tool called: ${tc.toolName}`),
    );
    agentResponse =
      toolCallSummaries.length > 0
        ? `The agent invoked the following tools to answer the question but the data layer did not return a final text summary: ${toolCallSummaries.join(', ')}.`
        : 'The agent completed its analysis but did not produce a textual summary.';
  }

  console.log('Agent response:', agentResponse);

  // Persist the response to response.json
  const outputPath = path.join(__dirname, 'response.json');
  await fs.writeFile(outputPath, JSON.stringify({ response: agentResponse }, null, 2), 'utf-8');
  console.log(`Response saved to ${outputPath}`);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
