const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

async function run() {
  // Initialize the client
  // Note: An API key is required in a real scenario, usually via INCONVO_API_KEY env var
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY || 'your_api_key_here'
  });

  try {
    // Create a conversation
    console.log('Creating conversation...');
    const conversation = await client.conversations.create();

    // Send a natural language query
    console.log('Sending query: "What are my top products?"');
    const response = await conversation.sendMessage('What are my top products?');

    // Extract the table response
    // The response structure typically includes messages, and one of them might be a table
    // For this example, we'll assume the response object or its data property contains the table
    const tableData = response.data || response;

    // Write to response.json
    const outputPath = path.join(__dirname, 'response.json');
    fs.writeFileSync(outputPath, JSON.stringify(tableData, null, 2));

    console.log(`Response logged to ${outputPath}`);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

run();
