import { streamText } from "ai";
import { gateway } from "@ai-sdk/gateway";
import { inconvoDataAgent } from "@inconvoai/vercel-ai-sdk";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const tools = inconvoDataAgent({
    agentId: process.env.INCONVO_AGENT_ID!,
    userIdentifier: "user-123",
    userContext: {
      organisationId: 1,
    },
  });

  const result = streamText({
    model: gateway("openai/gpt-4o-mini"),
    messages,
    tools,
  });

  return result.toUIMessageStreamResponse();
}
