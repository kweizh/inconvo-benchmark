import Inconvo from "@inconvoai/node";
import fs from "node:fs";

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
  const conversation = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    { userIdentifier: "user-pii-off-test" },
  );
  const response = await inconvo.agents.conversations.response.create(
    conversation.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "List customer names and their total orders",
      stream: false,
    },
  );
  fs.writeFileSync("response.json", JSON.stringify(response, null, 2));
}

main().catch((err) => { console.error(err); process.exit(1); });