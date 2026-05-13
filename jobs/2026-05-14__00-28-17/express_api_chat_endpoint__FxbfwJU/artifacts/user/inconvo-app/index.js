require('dotenv').config();
const express = require('express');
const { Inconvo } = require('@inconvoai/node');

const app = express();
app.use(express.json());

const PORT = 3001;

app.post('/chat', async (req, res) => {
  const { message, userId } = req.body;

  if (!message || typeof message !== 'string' || message.trim() === '') {
    return res.status(400).json({ error: 'message is required' });
  }

  try {
    const inconvo = new Inconvo({
      apiKey: process.env.INCONVO_API_KEY,
    });

    const agentId = process.env.INCONVO_AGENT_ID;

    // 2. Call inconvo.agents.conversations.create
    const conversation = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: userId,
      userContext: { organisationId: 1 }
    });

    // 3. Call inconvo.agents.conversations.response.create
    const response = await inconvo.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: message,
      stream: false
    });

    // 4. Send the response object returned by Inconvo back to the client
    res.status(200).json(response);
  } catch (error) {
    console.error('Inconvo API error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
