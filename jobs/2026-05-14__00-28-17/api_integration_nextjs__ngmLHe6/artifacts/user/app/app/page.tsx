'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
      <div className="space-y-4">
        {messages.map(m => (
          <div key={m.id} className="whitespace-pre-wrap">
            <div>
              <span className="font-bold">{m.role === 'user' ? 'User: ' : 'AI: '}</span>
              {m.content}
            </div>
            {m.toolInvocations?.map((toolInvocation) => {
              const { toolName, toolCallId, state } = toolInvocation;

              if (toolName === 'inconvo' && (state === 'result' || (state as string) === 'output-available')) {
                return (
                  <div key={toolCallId} data-testid="inconvo-result">
                    Data Visualization Available
                  </div>
                );
              }

              return null;
            })}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Ask about your data..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
