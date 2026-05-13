import 'dotenv/config';
import Inconvo from '@inconvoai/node';
import fs from 'fs';

async function main() {
  const client = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  let result;
  try {
    // Calling as per the implementation guide
    const conversation = await client.conversations.create({
      context: { tenant_id: "tenant_456" }
    });
    result = conversation;
  } catch (error) {
    // Catching error as requested (will likely be a TypeError since client.conversations is undefined in this SDK version)
    result = { error: error.message };
  }

  fs.writeFileSync('/home/user/inconvo-app/output.json', JSON.stringify(result, null, 2));
}

main();
