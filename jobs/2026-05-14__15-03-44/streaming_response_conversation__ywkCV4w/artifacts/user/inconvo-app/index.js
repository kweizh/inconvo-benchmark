import 'dotenv/config';
import Inconvo from '@inconvoai/node';
import fs from 'fs';

// Initialize Inconvo client with API key from environment
const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY
});

async function main() {
  console.log('Starting Inconvo Data Agent streaming...');

  // Create a conversation
  const conv = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {
      userIdentifier: 'stream-user'
    }
  );

  console.log('Created conversation:', conv.id);

  // Initialize stream file (truncate if exists)
  const streamPath = '/home/user/inconvo-app/stream.jsonl';
  const streamFile = fs.createWriteStream(streamPath, { flags: 'w' });

  let chunkCount = 0;
  let finalMessage = '';

  // Create streaming response with stream: true
  const stream = inconvo.agents.conversations.response.create(conv.id, {
    agentId: process.env.INCONVO_AGENT_ID,
    message: 'Summarize our sales trends for the last 3 months',
    stream: true
  });

  // Iterate through stream events
  for await (const chunk of stream) {
    chunkCount++;
    // Write each chunk as a single JSON line
    streamFile.write(JSON.stringify(chunk) + '\n');

    // Capture final message from response.completed event
    if (chunk.type === 'response.completed') {
      // Extract message from the response
      if (chunk.response.message && typeof chunk.response.message === 'string') {
        finalMessage = chunk.response.message;
      } else {
        finalMessage = JSON.stringify(chunk.response);
      }
    }
  }

  streamFile.end();

  // Write summary file with chunk count and final message
  const summary = {
    chunkCount,
    finalMessage
  };

  fs.writeFileSync('/home/user/inconvo-app/summary.json', JSON.stringify(summary, null, 2));

  console.log('Stream complete. Total chunks:', chunkCount);
  console.log('Final message:', finalMessage);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});