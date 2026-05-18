import { streamText } from 'ai';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';
import { openai } from '@ai-sdk/openai';

export const runtime = 'edge';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
      inconvoDataAgent: inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID || '',
        userIdentifier: 'user-123',
        userContext: {
          organisationId: 1,
        },
      }) as any,
    },
  });

  return result.toUIMessageStreamResponse();
}