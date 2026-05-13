const fs = require('fs');
const path = require('path');
require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');

async function main() {
  const apiKey = process.env.INCONVO_API_KEY;
  const agentId = process.env.INCONVO_AGENT_ID;

  if (!apiKey || !agentId) {
    console.error('Missing environment variables INCONVO_API_KEY or INCONVO_AGENT_ID');
    process.exit(1);
  }

  const inconvo = new Inconvo({ apiKey });

  try {
    // 3. Create a new conversation
    console.log('Creating conversation...');
    const conversation = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: 'user-123',
      userContext: { organisationId: 1, store_id: 1 }
    });

    const convId = conversation.id;
    console.log(`Conversation created with ID: ${convId}`);

    // 4. Write the conversation id to conversation_id.txt
    fs.writeFileSync(path.join(__dirname, 'conversation_id.txt'), convId);

    // 5. Send the FIRST message
    console.log('Sending first message...');
    const firstResponse = await inconvo.agents.conversations.response.create(convId, {
      agentId: agentId,
      message: "Show me my top 5 customers by total order amount.",
      stream: false
    });

    fs.writeFileSync(
      path.join(__dirname, 'first_response.json'),
      JSON.stringify(firstResponse, null, 2)
    );

    // 6. Send the FOLLOWUP message on the SAME conversation id
    console.log('Sending second message...');
    const secondResponse = await inconvo.agents.conversations.response.create(convId, {
      agentId: agentId,
      message: "Now show me only those located in the United States.",
      stream: false
    });

    fs.writeFileSync(
      path.join(__dirname, 'second_response.json'),
      JSON.stringify(secondResponse, null, 2)
    );

    console.log('Done.');
    process.exit(0);
  } catch (error) {
    console.error('Error during conversation flow:', error);
    process.exit(1);
  }
}

main();
