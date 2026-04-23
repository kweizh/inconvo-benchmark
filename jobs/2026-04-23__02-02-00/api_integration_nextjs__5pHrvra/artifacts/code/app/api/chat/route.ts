import { streamText } from 'ai';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o' as any,
    tools: {
      ...inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID!,
        userIdentifier: 'user-123',
        userContext: { organisationId: 1 },
      }),
    },
    messages,
  });

  return result.toUIMessageStreamResponse();
}
