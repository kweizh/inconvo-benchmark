'use client';

import { useChat } from '@ai-sdk/react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
      <div className="flex-1 overflow-y-auto mb-8">
        {messages.map((m) => (
          <div key={m.id} className="mb-4">
            <div className="font-bold">{m.role === 'user' ? 'User' : 'AI'}</div>
            <div className="whitespace-pre-wrap">{m.content}</div>
            {m.toolInvocations?.map((toolInvocation: any) => {
              const { toolCallId, toolName, state } = toolInvocation;

              if (
                state === 'output-available' &&
                [
                  'getDataAgentConnectedDataSummary',
                  'startDataAgentConversation',
                  'messageDataAgent',
                ].includes(toolName)
              ) {
                return (
                  <div key={toolCallId} data-testid="inconvo-result" className="mt-2 p-2 bg-gray-100 rounded">
                    Data Visualization Available
                  </div>
                );
              }

              return null;
            })}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="fixed bottom-0 w-full max-w-md">
        <input
          className="w-full p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Ask about your data..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
