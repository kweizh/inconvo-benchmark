import Inconvo from "@inconvoai/node";
import dotenv from "dotenv";
import fs from "fs";
import path from "path";

dotenv.config();

const apiKey = process.env.INCONVO_API_KEY;
const agentId = process.env.INCONVO_AGENT_ID;

if (!apiKey || !agentId) {
  console.error("Missing INCONVO_API_KEY or INCONVO_AGENT_ID environment variables");
  process.exit(1);
}

const inconvo = new Inconvo({ apiKey });

const streamFilePath = "/home/user/inconvo-app/stream.jsonl";
const summaryFilePath = "/home/user/inconvo-app/summary.json";

// Truncate stream.jsonl at the start
fs.writeFileSync(streamFilePath, "");

async function run() {
  try {
    // 1. Create a conversation
    const conv = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: "stream-user",
      userContext: { organisationId: 1, store_id: 1 },
    });

    console.log(`Created conversation: ${conv.id}`);

    // 2. Create a streaming response
    const stream = await inconvo.agents.conversations.response.create(conv.id, {
      agentId: agentId,
      message: "Summarize our sales trends for the last 3 months",
      stream: true,
    });

    let chunkCount = 0;
    let finalMessage = "";

    // 3. Iterate the stream
    for await (const chunk of stream) {
      chunkCount++;
      fs.appendFileSync(streamFilePath, JSON.stringify(chunk) + "\n");

      if (chunk.type === "response.completed") {
        if (chunk.response && chunk.response.message) {
          finalMessage = chunk.response.message;
        } else {
          finalMessage = JSON.stringify(chunk.response);
        }
      }
    }

    // 4. Write summary
    const summary = {
      chunkCount,
      finalMessage,
    };
    fs.writeFileSync(summaryFilePath, JSON.stringify(summary, null, 2));

    console.log("Streaming session completed successfully.");
    console.log(`Summary written to ${summaryFilePath}`);
  } catch (error) {
    console.error("Error during streaming session:", error);
    process.exit(1);
  }
}

run();
