require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');

const client = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
  agentId: process.env.INCONVO_AGENT_ID,
});

console.log('Agents.conversations.response properties:', Object.getOwnPropertyNames(client.agents.conversations.response));
