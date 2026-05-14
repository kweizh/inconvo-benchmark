import "dotenv/config";
import { randomUUID } from "crypto";
import { createWriteStream } from "fs";
import { writeFile } from "fs/promises";
import { Inconvo } from "@inconvoai/node";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_PATH = path.join(__dirname, "output.json");

async function main() {
  const apiKey = process.env.INCONVO_API_KEY;
  const agentId = process.env.INCONVO_AGENT_ID;

  if (!apiKey || !agentId) {
    const error = {
      error: "Missing required environment variables: INCONVO_API_KEY and/or INCONVO_AGENT_ID",
    };
    await writeFile(OUTPUT_PATH, JSON.stringify(error, null, 2));
    console.error(error.error);
    return;
  }

  const client = new Inconvo({ apiKey });

  let conversationId;
  let result = {};

  try {
    // Step 1: Create a conversation with userContext { organisationId: 2 }
    const conversation = await client.agents.conversations.create(agentId, {
      userIdentifier: randomUUID().toString(),
      userContext: { organisationId: 2 },
    });

    conversationId = conversation.id;
    result.conversation = conversation;

    // Step 2: Send a natural language query and receive a structured response
    const response = await client.agents.conversations.response.create(
      conversationId,
      {
        agentId,
        message: "QUERY",
      }
    );

    result.response = response;

    await writeFile(OUTPUT_PATH, JSON.stringify(result, null, 2));
    console.log("Success! Output written to output.json");
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    const errorOutput = {
      error: err.message || String(err),
      ...(err.status !== undefined && { status: err.status }),
      ...(err.headers !== undefined && { headers: Object.fromEntries(err.headers) }),
      ...(result.conversation !== undefined && { conversation: result.conversation }),
    };
    await writeFile(OUTPUT_PATH, JSON.stringify(errorOutput, null, 2));
    console.error("Error captured and written to output.json:");
    console.error(JSON.stringify(errorOutput, null, 2));
  }
}

main();
