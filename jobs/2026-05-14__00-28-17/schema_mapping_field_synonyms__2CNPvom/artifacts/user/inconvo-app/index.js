require("dotenv").config();
const { randomUUID } = require("node:crypto");
const fs = require("node:fs");
const Inconvo = require("@inconvoai/node").default;

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
  const convo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    { 
      userIdentifier: randomUUID().toString(),
      userContext: {
        store_id: 1
      }
    }
  );
  const response = await inconvo.agents.conversations.response.create(
    convo.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "What is the total revenue per buyer?",
      stream: false,
    }
  );
  fs.writeFileSync("response.json", JSON.stringify(response, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
