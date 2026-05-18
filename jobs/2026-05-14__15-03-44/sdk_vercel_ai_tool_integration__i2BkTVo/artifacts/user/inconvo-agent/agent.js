import 'dotenv/config';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import Inconvo from '@inconvoai/node';
import {
  getDataAgentConnectedDataSummary
} from '@inconvoai/vercel-ai-sdk';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  console.log('Initializing Inconvo agent...');

  // Read environment variables
  const inconvoApiKey = process.env.INCONVO_API_KEY;
  const inconvoAgentId = process.env.INCONVO_AGENT_ID;
  const inconvoDbUrl = process.env.INCONVO_DB_URL;
  const openaiApiKey = process.env.OPENAI_API_KEY;

  if (!inconvoApiKey || !inconvoAgentId || !inconvoDbUrl || !openaiApiKey) {
    throw new Error('Missing required environment variables. Please ensure INCONVO_API_KEY, INCONVO_AGENT_ID, INCONVO_DB_URL, and OPENAI_API_KEY are set.');
  }

  console.log('Environment variables loaded successfully');
  console.log('Agent ID:', inconvoAgentId);

  // Initialize Inconvo client
  const inconvo = new Inconvo({
    apiKey: inconvoApiKey
  });

  console.log('Inconvo client initialized');

  // Step 1: Get data summary (optional, but useful for understanding the data)
  console.log('\nStep 1: Getting data summary...');
  const dataSummaryTool = getDataAgentConnectedDataSummary({
    inconvo,
    agentId: inconvoAgentId
  });

  try {
    const dataSummaryResult = await dataSummaryTool.execute({});
    console.log('Data summary:', JSON.stringify(dataSummaryResult, null, 2));
  } catch (error) {
    console.log('Could not get data summary (this might be expected):', error.message);
  }

  // Step 2: Start a conversation directly using Inconvo API
  console.log('\nStep 2: Starting conversation...');
  const conversation = await inconvo.agents.conversations.create(inconvoAgentId, {
    userIdentifier: 'system-user'
  });
  console.log('Conversation started:', JSON.stringify(conversation, null, 2));

  if (!conversation?.id) {
    throw new Error('Failed to start conversation: no conversation ID returned');
  }

  const conversationId = conversation.id;
  console.log('Conversation ID:', conversationId);

  // Step 3: Ask the question directly using Inconvo API
  console.log('\nStep 3: Asking question about total orders...');
  const stream = inconvo.agents.conversations.response.create(conversationId, {
    agentId: inconvoAgentId,
    message: 'What is the total amount of orders?',
    stream: true
  });

  let finalResponse = null;
  let chunks = [];

  try {
    for await (const chunk of stream) {
      console.log('Chunk received:', chunk.type);
      chunks.push(chunk);

      if (chunk.type === 'response.completed') {
        finalResponse = chunk.response;
        console.log('Response completed!');
        break;
      }
    }

    if (!finalResponse) {
      console.log('No response.completed event received. Chunks received:', chunks.length);
      console.log('Chunks:', JSON.stringify(chunks, null, 2));
      throw new Error('No response received from Inconvo');
    }

    console.log('Final response:', JSON.stringify(finalResponse, null, 2));
  } catch (error) {
    console.error('Error during streaming:', error.message);
    console.error('Chunks received:', chunks.length);
    console.error('Chunks:', JSON.stringify(chunks, null, 2));
    throw error;
  }

  // Step 4: Use OpenAI to format the response
  console.log('\nStep 4: Formatting response with OpenAI...');
  const formattedResponse = await generateText({
    model: openai('gpt-4o'),
    prompt: `Please provide a clear, natural language answer to the user's question based on the following data analysis result:

User's question: "What is the total amount of orders?"

Data analysis result:
${JSON.stringify(finalResponse, null, 2)}

Provide a concise, helpful answer.`,
    temperature: 0
  });

  console.log('Formatted response:', formattedResponse.text);

  // Save response to response.json
  const responseObj = {
    response: formattedResponse.text
  };

  const responsePath = path.join(__dirname, 'response.json');
  fs.writeFileSync(responsePath, JSON.stringify(responseObj, null, 2), 'utf-8');
  console.log(`\nResponse saved to ${responsePath}`);

  return formattedResponse.text;
}

// Run the main function
main()
  .then(() => {
    console.log('\nAgent completed successfully');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\nError:', error.message);
    console.error(error.stack);
    process.exit(1);
  });