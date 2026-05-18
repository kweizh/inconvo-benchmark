require('dotenv').config();
const express = require('express');
const Inconvo = require('@inconvoai/node');

const app = express();

// Parse JSON request bodies
app.use(express.json());

// POST /chat endpoint
app.post('/chat', async (req, res) => {
  const { message, userId } = req.body;

  // Validate that message is present and non-empty
  if (!message || message.trim() === '') {
    return res.status(400).json({ error: 'message is required' });
  }

  try {
    // Initialize Inconvo client
    const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

    // Create a new agent conversation
    const conversation = await inconvo.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {
        userIdentifier: userId,
        userContext: { organisationId: 1 }
      }
    );

    // Get the agent response
    const response = await inconvo.agents.conversations.response.create(
      conversation.id,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message,
        stream: false
      }
    );

    // Send response back to the client
    res.status(200).json(response);
  } catch (error) {
    console.error('Error processing chat request:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start server on port 3001
app.listen(3001, () => {
  console.log('Server is running on port 3001');
});