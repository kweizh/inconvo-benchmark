import fs from 'fs';
import path from 'path';
import * as dotenv from 'dotenv';
import Inconvo from '@inconvoai/node';

dotenv.config();

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const conv = await inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
    userIdentifier: "stream-user",
    userContext: { organisationId: 1, store_id: 1 }
  });

  const stream = await inconvo.agents.conversations.response.create(conv.id, {
    agentId: process.env.INCONVO_AGENT_ID,
    message: "Summarize our sales trends for the last 3 months",
    stream: true
  });

  const streamFilePath = path.join(process.cwd(), 'stream.jsonl');
  const summaryFilePath = path.join(process.cwd(), 'summary.json');

  // Truncate stream.jsonl
  fs.writeFileSync(streamFilePath, '');

  let chunkCount = 0;
  let finalMessage = "";

  for await (const chunk of stream) {
    chunkCount++;
    fs.appendFileSync(streamFilePath, JSON.stringify(chunk) + "\n");
    
    // The event property might be 'type' or 'event'
    if (chunk.type === 'response.completed' || chunk.event === 'response.completed') {
      if (chunk.response && typeof chunk.response.message === 'string') {
        finalMessage = chunk.response.message;
      } else {
        finalMessage = JSON.stringify(chunk.response || chunk);
      }
    }
  }

  // Write summary
  fs.writeFileSync(summaryFilePath, JSON.stringify({
    chunkCount,
    finalMessage
  }));
}

main().catch(console.error);
