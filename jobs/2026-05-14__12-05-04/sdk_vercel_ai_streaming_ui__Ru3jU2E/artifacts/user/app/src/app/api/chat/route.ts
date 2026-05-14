import { Inconvo } from '@inconvoai/node';
import { InconvoResponse } from '@inconvoai/vercel-ai-sdk';
import { StreamData, toDataStreamResponse } from 'ai';

export const dynamic = 'force-dynamic';

export async function POST(req: Request) {
  const { messages } = await req.json();
  const lastMessage = messages[messages.length - 1];

  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY!,
  });

  // Create a conversation for the user
  // In a real application, you might want to persist and reuse conversation IDs
  const conversation = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID!,
    {
      userIdentifier: 'user-123',
    }
  );

  // Start the streaming response from Inconvo
  const stream = inconvo.agents.conversations.response.create(
    conversation.id!,
    {
      agentId: process.env.INCONVO_AGENT_ID!,
      message: lastMessage.content,
      stream: true,
    }
  );

  const data = new StreamData();

  const readableStream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();
      try {
        for await (const event of stream) {
          if (event.type === 'response.progress') {
            // Send text progress to the client
            controller.enqueue(encoder.encode(`0:${JSON.stringify(event.message)}\n`));
          } else if (event.type === 'response.completed') {
            // If the response contains a table, send it as data
            if (event.response.type === 'table' && event.response.table) {
              data.append({
                type: 'table',
                table: event.response.table,
              });
            }
          }
        }
      } catch (error) {
        console.error('Error streaming from Inconvo:', error);
      } finally {
        data.close();
        controller.close();
      }
    },
  });

  return toDataStreamResponse(readableStream, { data });
}
