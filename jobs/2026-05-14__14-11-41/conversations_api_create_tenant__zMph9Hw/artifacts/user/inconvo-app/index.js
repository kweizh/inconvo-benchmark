const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');
const { randomUUID } = require('crypto');
require('dotenv').config();

async function main() {
  try {
    const client = new Inconvo({
      apiKey: process.env.INCONVO_API_KEY
    });

    const agentId = process.env.INCONVO_AGENT_ID;

    // Create a conversation using the client with the UserContext {"organisationId": 2}
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: randomUUID().toString(),
      userContext: { organisationId: 2 }
    });

    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "QUERY"
    });

    // Save the resulting conversation object
    fs.writeFileSync('/home/user/inconvo-app/output.json', JSON.stringify(conversation, null, 2));
  } catch (error) {
    // Write the error message or the response
    const errorData = error.response ? error.response : { error: error.message };
    fs.writeFileSync('/home/user/inconvo-app/output.json', JSON.stringify(errorData, null, 2));
  }
}

main();
