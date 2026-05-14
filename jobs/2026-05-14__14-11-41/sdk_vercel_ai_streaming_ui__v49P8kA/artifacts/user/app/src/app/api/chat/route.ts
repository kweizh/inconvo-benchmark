import { streamText, stepCountIs } from 'ai';
import { gateway } from 'ai';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: gateway('openai/gpt-4o-mini'),
    messages,
    tools: inconvoDataAgent({
      agentId: process.env.INCONVO_AGENT_ID!,
      userIdentifier: 'user-123',
      userContext: {},
    }),
    stopWhen: stepCountIs(5),
  });

  return result.toUIMessageStreamResponse();
}
