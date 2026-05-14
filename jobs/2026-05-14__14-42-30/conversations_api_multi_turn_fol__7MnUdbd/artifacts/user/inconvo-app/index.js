import 'dotenv/config';
import Inconvo from '@inconvoai/node';
import fs from 'fs';

async function main() {
  // 1. Initialize the Inconvo client with INCONVO_API_KEY
  const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

  // 2. Create a new conversation against INCONVO_AGENT_ID with userContext
  const conversation = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {
      userIdentifier: 'user_1',
    }
  );

  const convId = conversation.id;
  console.log('Conversation created:', convId);

  // 3. Write the conversation id to conversation_id.txt
  fs.writeFileSync('/home/user/inconvo-app/conversation_id.txt', convId);

  // 4. Send the first message (non-streaming)
  const firstResponse = await inconvo.agents.conversations.response.create(
    convId,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: 'Show me my top 5 customers by total order amount.',
      stream: false,
    }
  );

  console.log('First response received.');

  // 5. Write first response to first_response.json
  fs.writeFileSync(
    '/home/user/inconvo-app/first_response.json',
    JSON.stringify(firstResponse, null, 2)
  );

  // 6. Send the followup message on the SAME conversation id (non-streaming)
  const secondResponse = await inconvo.agents.conversations.response.create(
    convId,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: 'Now show me only those located in the United States.',
      stream: false,
    }
  );

  console.log('Second response received.');

  // 7. Write second response to second_response.json
  fs.writeFileSync(
    '/home/user/inconvo-app/second_response.json',
    JSON.stringify(secondResponse, null, 2)
  );

  console.log('Done. All artifacts written successfully.');
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
