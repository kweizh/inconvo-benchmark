import { Inconvo } from '@inconvoai/node';
import { InconvoStream } from '@inconvoai/vercel-ai-sdk';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY!,
  });

  const response = await inconvo.chat.completions.create({
    agentId: process.env.INCONVO_AGENT_ID!,
    messages,
    stream: true,
  });

  return InconvoStream(response);
}
