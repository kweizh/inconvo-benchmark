const express = require('express');
const { Inconvo } = require('@inconvoai/node');

const app = express();
app.use(express.json());

const apiKey = process.env.INCONVO_API_KEY;
const agentId = process.env.INCONVO_AGENT_ID;

if (!apiKey || !agentId) {
  console.error('Missing INCONVO_API_KEY or INCONVO_AGENT_ID environment variables');
  process.exit(1);
}

const client = new Inconvo({
  apiKey: apiKey,
});

app.post('/ask', async (req, res) => {
  const { question, userId } = req.body;

  if (!question || !userId) {
    return res.status(400).json({ error: 'Missing question or userId in request body' });
  }

  try {
    // 6. Create a conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: userId,
    });

    // 7. Send the message
    const response = await client.agents.conversations.response.create(
      conversation.id,
      {
        agentId: agentId,
        message: question,
      }
    );

    res.json(response);
  } catch (error) {
    console.error('Error interacting with Inconvo:', error);
    res.status(500).json({ error: 'Failed to process request', details: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
