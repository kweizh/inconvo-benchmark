'use strict';

require('dotenv').config();

const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function main() {
  const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

  const conversation = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    { userIdentifier: 'user_1' }
  );

  const conversationId = conversation.id;

  const response = await inconvo.agents.conversations.response.create(
    conversationId,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: 'What is the average gross margin per month?',
      stream: false,
    }
  );

  const outputPath = path.join(__dirname, 'response.json');
  fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
  console.log('Response written to', outputPath);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
