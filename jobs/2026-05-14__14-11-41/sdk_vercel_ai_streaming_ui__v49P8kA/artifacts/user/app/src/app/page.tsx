'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div className="flex flex-col w-full max-w-2xl py-24 mx-auto stretch">
      {messages.map(m => (
        <div key={m.id} className="whitespace-pre-wrap mb-6">
          <strong>{m.role === 'user' ? 'User: ' : 'AI: '}</strong>
          {m.content}
          
          {m.toolInvocations?.map(toolInvocation => {
            const toolCallId = toolInvocation.toolCallId;
            
            if (!('result' in toolInvocation)) {
              return (
                <div key={toolCallId} className="mt-2 text-gray-500 italic text-sm">
                  Calling {toolInvocation.toolName}...
                </div>
              );
            }

            const result = toolInvocation.result;

            if (toolInvocation.toolName === 'messageDataAgent' && result && typeof result === 'object' && 'type' in result) {
              if (result.type === 'table' && result.table) {
                return (
                  <div key={toolCallId} className="mt-4 overflow-x-auto">
                    <table className="min-w-full border-collapse border border-gray-300 text-sm">
                      <thead>
                        <tr>
                          {result.table.head.map((header: string, i: number) => (
                            <th key={i} className="border border-gray-300 px-4 py-2 bg-gray-100 dark:bg-gray-800 text-left font-semibold">
                              {header}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {result.table.body.map((row: string[], i: number) => (
                          <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-900">
                            {row.map((cell: string, j: number) => (
                              <td key={j} className="border border-gray-300 px-4 py-2">
                                {cell}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                );
              }
              
              if (result.type === 'text' && result.message) {
                return (
                  <div key={toolCallId} className="mt-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-md">
                    {result.message}
                  </div>
                );
              }
            }
            
            return (
              <div key={toolCallId} className="mt-2 text-green-600 italic text-sm">
                Completed {toolInvocation.toolName}.
              </div>
            );
          })}
        </div>
      ))}

      <form onSubmit={handleSubmit} className="fixed bottom-0 w-full max-w-2xl p-2 mb-8 border border-gray-300 rounded shadow-xl bg-white dark:bg-black">
        <input
          className="w-full p-2 bg-transparent outline-none text-black dark:text-white"
          value={input}
          placeholder="Ask a question about your data..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
