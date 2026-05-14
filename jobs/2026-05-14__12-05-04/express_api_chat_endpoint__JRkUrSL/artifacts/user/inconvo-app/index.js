require('dotenv').config();
const express = require('express');
const Inconvo = require('@inconvoai/node');

const app = express();
app.use(express.json());

const PORT = 3001;

app.post('/chat', async (req, res) => {
  const { message, userId } = req.body;

  if (!message || message.trim() === '') {
    return res.status(400).json({ error: 'message is required' });
  }

  try {
    const inconvo = new Inconvo({
      apiKey: process.env.INCONVO_API_KEY,
    });

    const conversation = await inconvo.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {
        userIdentifier: userId,
        userContext: { organisationId: 1 },
      }
    );

    const response = await inconvo.agents.conversations.response.create(
      conversation.id,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message,
        stream: false,
      }
    );

    res.status(200).json(response);
  } catch (error) {
    console.error('Error in /chat:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
