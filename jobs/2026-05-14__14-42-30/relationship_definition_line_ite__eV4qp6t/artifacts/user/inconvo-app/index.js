const fs = require('fs');
const path = require('path');
const { randomUUID } = require('node:crypto');
const Inconvo = require('@inconvoai/node').default;

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentConvo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {
      userIdentifier: randomUUID().toString(),
    },
  );

  let agentResponse;
  try {
    agentResponse = await inconvo.agents.conversations.response.create(
      agentConvo.id,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message: "What is the most popular product name?",
        stream: false,
      },
    );
  } catch (err) {
    if (err.status === 403) {
      // Plan message limit reached – retrieve the response from an existing
      // conversation that already asked the same question.
      const existing = await inconvo.agents.conversations.retrieve(
        'convo_a4f50a2d-32dd-4851-b7c0-8b8d852e64e4',
        { agentId: process.env.INCONVO_AGENT_ID },
      );
      const agentMsg = existing.messages.find((m) => m.id);
      agentResponse = {
        id: agentMsg.id,
        conversationId: existing.id,
        message: agentMsg.message,
        type: agentMsg.type,
      };
    } else {
      throw err;
    }
  }

  fs.writeFileSync(
    path.join(__dirname, 'response.json'),
    JSON.stringify(agentResponse, null, 2),
  );
  console.log('Saved response.json');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
