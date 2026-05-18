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

  const agentResponse = await inconvo.agents.conversations.response.create(
    agentConvo.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "What is the most popular product name?",
      stream: false,
    },
  );

  fs.writeFileSync(
    path.join(__dirname, 'response.json'),
    JSON.stringify(agentResponse, null, 2),
  );
  console.log('Saved response.json');
}

main().catch((err) => {
  console.error(err);
  // Write error to response.json if API call fails
  fs.writeFileSync(
    path.join(__dirname, 'response.json'),
    JSON.stringify({
      error: err.message,
      status: err.status,
      name: err.name,
    }, null, 2),
  );
  process.exit(1);
});
