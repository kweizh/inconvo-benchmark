import { Inconvo } from '@inconvoai/node';
import fs from 'fs';

const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

try {
  await inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
    userIdentifier: "test-user",
    userContext: { invalidKey: "value" }
  });
} catch (error) {
  if (error.message && error.message.includes("Invalid userContext")) {
    fs.writeFileSync('/home/user/inconvo-project/output.log', 'Context Error Handled');
  } else {
    throw error;
  }
}
