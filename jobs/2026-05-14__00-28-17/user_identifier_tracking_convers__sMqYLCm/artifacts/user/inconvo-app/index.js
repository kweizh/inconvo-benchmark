import "dotenv/config";
import Inconvo from "@inconvoai/node";
import fs from "node:fs";
import path from "node:path";

const BASE_DIR = "/home/user/inconvo-app";
const USERS_FILE = path.join(BASE_DIR, "users.json");
const RESPONSES_DIR = path.join(BASE_DIR, "responses");
const CONV_IDS_FILE = path.join(BASE_DIR, "conversation_ids.json");

async function main() {
  const users = JSON.parse(fs.readFileSync(USERS_FILE, "utf-8"));
  const client = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });
  const agentId = process.env.INCONVO_AGENT_ID;

  if (!fs.existsSync(RESPONSES_DIR)) {
    fs.mkdirSync(RESPONSES_DIR, { recursive: true });
  }

  const conversationIds = {};

  for (const id of users) {
    console.log(`Creating conversation for user: ${id}`);
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: id,
      userContext: { organisationId: 1, store_id: 1 },
    });

    console.log(`Sending message for user: ${id}`);
    const response = await client.agents.conversations.response.create(conversation.id, {
      agentId: agentId,
      message: "Hello, what is my latest order amount?",
      stream: false,
    });

    fs.writeFileSync(
      path.join(RESPONSES_DIR, `${id}.json`),
      JSON.stringify(response, null, 2)
    );

    conversationIds[id] = conversation.id;
  }

  fs.writeFileSync(CONV_IDS_FILE, JSON.stringify(conversationIds, null, 2));
  console.log("Done!");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
