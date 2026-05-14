import { streamText, stepCountIs, gateway, convertToModelMessages } from "ai";
import { inconvoDataAgent } from "@inconvoai/vercel-ai-sdk";

export const runtime = "nodejs";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const modelMessages = await convertToModelMessages(messages);

  const result = streamText({
    model: gateway("openai/gpt-4o-mini"),
    system:
      "You are a helpful data assistant. Use the available tools to answer data questions. When the messageDataAgent tool returns a table result, include it verbatim in your response so the frontend can render it.",
    messages: modelMessages,
    tools: {
      ...inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID!,
        userIdentifier: "user-123",
        userContext: {},
      }),
    },
    stopWhen: stepCountIs(10),
  });

  return result.toUIMessageStreamResponse();
}
