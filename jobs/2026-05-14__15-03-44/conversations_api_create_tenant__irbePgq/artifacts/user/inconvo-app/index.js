import { Inconvo } from '@inconvoai/node';
import dotenv from 'dotenv';
import { randomUUID } from 'crypto';
import { writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function main() {
  try {
    // Initialize the Inconvo client
    const client = new Inconvo({
      apiKey: process.env.INCONVO_API_KEY,
    });

    // Create a conversation with tenant context
    const conversation = await client.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {
        userIdentifier: randomUUID().toString(),
        userContext: { organisationId: 2 }
      }
    );

    // Save the conversation object to output.json
    const outputPath = join(__dirname, 'output.json');
    writeFileSync(outputPath, JSON.stringify(conversation, null, 2));
    console.log('Conversation created successfully!');
    console.log('Output saved to:', outputPath);

  } catch (error) {
    // Handle errors and write error message to output.json
    const outputPath = join(__dirname, 'output.json');
    const errorMessage = {
      error: true,
      message: error.message,
      stack: error.stack
    };
    writeFileSync(outputPath, JSON.stringify(errorMessage, null, 2));
    console.error('Error occurred:', error.message);
    console.error('Error details saved to:', outputPath);
  }
}

main();