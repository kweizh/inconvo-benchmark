'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const chatHelpers = useChat();

  const { messages } = chatHelpers;
  const input = (chatHelpers as any).input || '';
  const handleInputChange = (chatHelpers as any).handleInputChange || (() => {});
  const handleSubmit = (chatHelpers as any).handleSubmit || (() => {});

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((message) => {
          const msg = message as any;
          return (
            <div
              key={message.id}
              className={`p-4 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white ml-auto max-w-[80%]'
                  : 'bg-gray-200 text-gray-800 mr-auto max-w-[80%]'
              }`}
            >
              <div className="font-semibold mb-1">
                {msg.role === 'user' ? 'You' : 'AI'}
              </div>
              <div>{msg.content}</div>
              {msg.toolInvocations?.map((toolInvocation: any, index: number) => {
                const tool = 'toolName' in toolInvocation ? toolInvocation : null;
                if (
                  tool &&
                  tool.toolName === 'inconvoDataAgent' &&
                  tool.state === 'output-available' &&
                  'result' in tool
                ) {
                  return (
                    <div
                      key={index}
                      data-testid="inconvo-result"
                    >
                      Data Visualization Available
                    </div>
                  );
                }
                return null;
              })}
            </div>
          );
        })}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Ask about your data..."
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  );
}