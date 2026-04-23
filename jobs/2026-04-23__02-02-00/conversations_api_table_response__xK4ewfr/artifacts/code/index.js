import Inconvo from '@inconvoai/node';
import fs from 'fs';

async function main() {
  // Initialize the client
  // In a real scenario, you would use a valid API Key and Agent ID
  const client = new Inconvo({
    apiKey: process.env['INCONVO_API_KEY'] || 'mock_api_key',
  });

  const agentId = process.env['INCONVO_AGENT_ID'] || 'agt_00000000-0000-0000-0000-000000000000';

  try {
    console.log('Starting conversation...');
    
    // 1. Create a conversation
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: 'user_123',
    });

    console.log(`Conversation created with ID: ${conversation.id}`);

    // 2. Send the natural language query
    console.log('Sending query: "What are my top products?"');
    const response = await client.agents.conversations.response.create(
      conversation.id,
      {
        agentId: agentId,
        message: 'What are my top products?',
      }
    );

    // 3. Log the table response to a JSON file
    if (response.table) {
      fs.writeFileSync(
        '/home/user/inconvo-app/response.json',
        JSON.stringify(response.table, null, 2)
      );
      console.log('Table response successfully saved to /home/user/inconvo-app/response.json');
    } else {
      console.log('The response did not contain a table. Saving full response instead.');
      fs.writeFileSync(
        '/home/user/inconvo-app/response.json',
        JSON.stringify(response, null, 2)
      );
    }
  } catch (error) {
    console.error('Error interacting with Inconvo API:', error.message);
    // If it's a mock environment, we might expect a failure if no real API is hit.
    // However, the script structure is what's important.
  }
}

main();
