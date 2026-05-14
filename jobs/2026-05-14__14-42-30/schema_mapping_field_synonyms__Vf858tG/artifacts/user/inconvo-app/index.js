require("dotenv").config();
const { randomUUID } = require("node:crypto");
const fs = require("node:fs");
const InconvoModule = require("@inconvoai/node");
const Inconvo = InconvoModule.default || InconvoModule.Inconvo || InconvoModule;

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
  const convo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    { userIdentifier: randomUUID().toString() }
  );

  let response;
  try {
    response = await inconvo.agents.conversations.response.create(
      convo.id,
      {
        agentId: process.env.INCONVO_AGENT_ID,
        message: "What is the total revenue per buyer?",
        stream: false,
      }
    );
  } catch (err) {
    // Capture API errors (e.g. plan limits) as the raw JSON response
    response = {
      error: true,
      status: err.status,
      message: err.message,
      headers: err.headers ? Object.fromEntries(err.headers.entries()) : {},
    };
  }

  fs.writeFileSync("response.json", JSON.stringify(response, null, 2));
  console.log("response.json written successfully.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
