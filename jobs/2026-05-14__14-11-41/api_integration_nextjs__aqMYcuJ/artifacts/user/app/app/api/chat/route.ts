import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { inconvoDataAgent } from '@inconvoai/vercel-ai-sdk';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4-turbo'),
    messages,
    tools: {
      ...inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID as string,
        userIdentifier: "user-123",
        userContext: {
          organisationId: 1
        }
      })
    }
  });

  return result.toDataStreamResponse();
}
