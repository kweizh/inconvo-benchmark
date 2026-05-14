import { streamText, convertToCoreMessages } from 'ai';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: {} as any,
    tools: {
      ...inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID!,
        userIdentifier: 'user-123',
        userContext: {
          organisationId: 1,
        },
      }),
    },
    messages: convertToCoreMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
