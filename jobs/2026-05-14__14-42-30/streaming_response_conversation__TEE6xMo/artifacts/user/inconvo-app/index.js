import "dotenv/config";
import fs from "fs";
import Inconvo from "@inconvoai/node";

const { INCONVO_API_KEY, INCONVO_AGENT_ID } = process.env;

if (!INCONVO_API_KEY) throw new Error("Missing env var: INCONVO_API_KEY");
if (!INCONVO_AGENT_ID) throw new Error("Missing env var: INCONVO_AGENT_ID");

const inconvo = new Inconvo({ apiKey: INCONVO_API_KEY });

// Create a new conversation
const conv = await inconvo.agents.conversations.create(INCONVO_AGENT_ID, {
  userIdentifier: "stream-user",
});

console.log(`Conversation created: ${conv.id}`);

// Open stream.jsonl for writing (truncate on each run)
const logPath = new URL("./stream.jsonl", import.meta.url).pathname;
const writeStream = fs.createWriteStream(logPath, { flags: "w" });

// Request a streaming response
const stream = inconvo.agents.conversations.response.create(conv.id, {
  agentId: INCONVO_AGENT_ID,
  message: "Summarize our sales trends for the last 3 months",
  stream: true,
});

let chunkCount = 0;
let finalMessage = "";

for await (const chunk of stream) {
  // Write each event as a single JSON line
  writeStream.write(JSON.stringify(chunk) + "\n");
  chunkCount++;

  console.log(`[${chunkCount}] event type: ${chunk.type}`);

  if (chunk.type === "response.completed") {
    const resp = chunk.response;
    finalMessage =
      typeof resp.message === "string" && resp.message.length > 0
        ? resp.message
        : JSON.stringify(resp);
  } else if (chunk.type === "error") {
    // Surface application-level stream errors in the final message
    finalMessage =
      typeof chunk.error === "string" && chunk.error.length > 0
        ? chunk.error
        : JSON.stringify(chunk);
  }
}

// Flush and close the log file
await new Promise((resolve, reject) => {
  writeStream.end((err) => (err ? reject(err) : resolve()));
});

// Write summary
const summaryPath = new URL("./summary.json", import.meta.url).pathname;
fs.writeFileSync(
  summaryPath,
  JSON.stringify({ chunkCount, finalMessage }, null, 2) + "\n",
  "utf8"
);

console.log(`\nStream complete.`);
console.log(`  Chunks received : ${chunkCount}`);
console.log(`  Final message   : ${finalMessage}`);
console.log(`  Log file        : ${logPath}`);
console.log(`  Summary file    : ${summaryPath}`);
