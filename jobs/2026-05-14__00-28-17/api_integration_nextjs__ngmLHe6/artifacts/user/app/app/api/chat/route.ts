import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    tools: {
      inconvo: inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID || '',
        userIdentifier: 'user-123',
        userContext: {
          organisationId: 1,
        },
      }) as any,
    },
    messages,
  });

  return result.toUIMessageStreamResponse();
}
