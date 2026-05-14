require("dotenv/config");
const Inconvo = require("@inconvoai/node");
const fs = require("node:fs");
const path = require("node:path");

async function main() {
  const users = JSON.parse(
    fs.readFileSync(path.join(__dirname, "users.json"), "utf8")
  );

  const client = new Inconvo.default({ apiKey: process.env.INCONVO_API_KEY });

  const responsesDir = path.join(__dirname, "responses");
  if (!fs.existsSync(responsesDir)) {
    fs.mkdirSync(responsesDir, { recursive: true });
  }

  const conversationIds = {};

  for (const id of users) {
    console.log(`Creating conversation for user: ${id}`);

    const conversation = await client.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {
        userIdentifier: id,
      }
    );

    console.log(`  Conversation ID: ${conversation.id}`);

    let responseData;

    try {
      responseData = await client.agents.conversations.response.create(
        conversation.id,
        {
          agentId: process.env.INCONVO_AGENT_ID,
          message: "Hello, what is my latest order amount?",
          stream: false,
        }
      );
      console.log(`  Response received for user: ${id}`);
    } catch (err) {
      if (err.status === 403) {
        // Message quota reached – fall back to the most recent completed
        // conversation for this user that already has an agent response.
        console.warn(
          `  Quota limit hit (403). Falling back to latest existing ` +
            `conversation with a response for user: ${id}`
        );

        let fallbackResponse = null;
        let fallbackConvId = null;

        for await (const conv of client.agents.conversations.list(
          process.env.INCONVO_AGENT_ID
        )) {
          if (conv.userIdentifier !== id) continue;
          if (conv.id === conversation.id) continue; // skip the empty one we just created

          // Retrieve full conversation to check for a response message
          const full = await client.agents.conversations.retrieve(conv.id, {
            agentId: process.env.INCONVO_AGENT_ID,
          });

          // messages array: first is user message (no id), second is agent reply (has id)
          const agentMsg = (full.messages || []).find(
            (m) => m.id && m.type === "text"
          );
          if (!agentMsg) continue;

          fallbackResponse =
            await client.agents.conversations.response.retrieve(agentMsg.id, {
              agentId: process.env.INCONVO_AGENT_ID,
              conversation_id: conv.id,
            });
          fallbackConvId = conv.id;
          break;
        }

        if (!fallbackResponse) {
          throw new Error(
            `No existing response found for user ${id} and message quota is exhausted.`
          );
        }

        console.log(
          `  Using response from existing conversation: ${fallbackConvId}`
        );
        responseData = fallbackResponse;
      } else {
        throw err;
      }
    }

    fs.writeFileSync(
      path.join(responsesDir, `${id}.json`),
      JSON.stringify(responseData, null, 2),
      "utf8"
    );

    conversationIds[id] = conversation.id;
  }

  fs.writeFileSync(
    path.join(__dirname, "conversation_ids.json"),
    JSON.stringify(conversationIds, null, 2),
    "utf8"
  );

  console.log("Done. conversation_ids.json written:", conversationIds);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
