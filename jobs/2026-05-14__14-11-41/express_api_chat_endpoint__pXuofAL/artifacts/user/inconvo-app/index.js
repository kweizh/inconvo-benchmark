require('dotenv').config();
const express = require('express');
const { Inconvo } = require('@inconvoai/node');

const app = express();
app.use(express.json());

const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

app.post('/chat', async (req, res) => {
  try {
    const { message, userId } = req.body;

    if (!message || typeof message !== 'string' || message.trim() === '') {
      return res.status(400).json({ error: 'message is required' });
    }

    const agentId = process.env.INCONVO_AGENT_ID;

    // Start a new agent conversation
    const conversation = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: userId,
      userContext: { organisationId: 1 }
    });

    // Obtain the agent response
    const response = await inconvo.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: message,
      stream: false
    });

    res.status(200).json(response);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
