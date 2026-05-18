import Inconvo from '@inconvoai/node';

// Initialize Inconvo client
const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    // Get the last user message
    const lastMessage = messages[messages.length - 1];
    
    if (!lastMessage || lastMessage.role !== 'user') {
      return new Response('Invalid message format', { status: 400 });
    }

    // Get Inconvo agent ID from environment
    const agentId = process.env.INCONVO_AGENT_ID;
    if (!agentId) {
      return new Response('INCONVO_AGENT_ID environment variable is not set', { 
        status: 500 
      });
    }

    // Create a new conversation
    const conversation = await inconvo.agents.conversations.create(agentId, {
      userIdentifier: 'default-user',
    });

    // Stream the response from Inconvo
    const stream = await inconvo.agents.conversations.response.create(
      conversation.id || '',
      {
        agentId,
        message: lastMessage.content,
        stream: true,
      }
    );

    // Convert Inconvo stream to Vercel AI SDK compatible format
    const encoder = new TextEncoder();
    
    const readableStream = new ReadableStream({
      async start(controller) {
        try {
          let fullText = '';
          
          for await (const event of stream) {
            if (event.type === 'response.progress') {
              // Stream text chunks
              const chunk = event.message;
              fullText += chunk;
              
              controller.enqueue(
                encoder.encode(`data: ${JSON.stringify({ 
                  type: 'text-delta',
                  textDelta: chunk 
                })}\n\n`)
              );
            } else if (event.type === 'response.completed') {
              const response = event.response;
              
              // Handle table responses
              if (response.type === 'table' && response.table) {
                const tableData = JSON.stringify({
                  type: 'table',
                  table: response.table,
                });
                
                controller.enqueue(
                  encoder.encode(`data: ${JSON.stringify({ 
                    type: 'data',
                    content: tableData,
                  })}\n\n`)
                );
              } 
              // Handle chart responses
              else if (response.type === 'chart' && response.chart) {
                const chartData = JSON.stringify({
                  type: 'chart',
                  chart: response.chart,
                });
                
                controller.enqueue(
                  encoder.encode(`data: ${JSON.stringify({ 
                    type: 'data',
                    content: chartData,
                  })}\n\n`)
                );
              }
              // Handle text responses
              else if (response.message && fullText === '') {
                // If we haven't streamed any text yet, send the full message
                controller.enqueue(
                  encoder.encode(`data: ${JSON.stringify({ 
                    type: 'text-delta',
                    textDelta: response.message 
                  })}\n\n`)
                );
              }
              
              // Send finish event
              controller.enqueue(
                encoder.encode(`data: ${JSON.stringify({ 
                  type: 'finish',
                  finishReason: 'stop',
                  usage: { promptTokens: 0, completionTokens: 0 },
                })}\n\n`)
              );
              
              controller.close();
            }
          }
        } catch (error) {
          console.error('Stream error:', error);
          controller.error(error);
        }
      },
    });

    return new Response(readableStream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Error in chat route:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to process chat message' }),
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}