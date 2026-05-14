import "dotenv/config";
import Inconvo from "@inconvoai/node";
import fs from "node:fs";
import path from "node:path";

async function main() {
  const usersPath = path.resolve("/home/user/inconvo-app/users.json");
  const users = JSON.parse(fs.readFileSync(usersPath, "utf-8"));
  
  const client = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });
  
  const responsesDir = path.resolve("/home/user/inconvo-app/responses");
  if (!fs.existsSync(responsesDir)) {
    fs.mkdirSync(responsesDir, { recursive: true });
  }

  const conversationIds = {};

  for (const id of users) {
    const userContext = { organisationId: 1 };
    userContext.store_id = 1; // Added to satisfy API validation
    const conversation = await client.agents.conversations.create(process.env.INCONVO_AGENT_ID, {
      userIdentifier: id,
      userContext
    });

    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "Hello, what is my latest order amount?",
      stream: false
    });

    fs.writeFileSync(
      path.join(responsesDir, `${id}.json`),
      JSON.stringify(response, null, 2)
    );

    conversationIds[id] = conversation.id;
  }

  fs.writeFileSync(
    path.resolve("/home/user/inconvo-app/conversation_ids.json"),
    JSON.stringify(conversationIds, null, 2)
  );
}

main().catch(console.error);
