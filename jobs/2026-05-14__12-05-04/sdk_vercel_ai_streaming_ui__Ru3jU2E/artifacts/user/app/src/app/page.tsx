'use client';

import { useChat } from 'ai/react';
import { useEffect, useRef } from 'react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, data, isLoading } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <header className="p-4 border-b border-gray-200 bg-white sticky top-0 z-10">
        <h1 className="text-xl font-bold text-gray-800 text-center">Inconvo Data Assistant</h1>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-lg">Welcome! Ask me anything about your data.</p>
            <p className="text-sm">Try: "Show me the sales by region"</p>
          </div>
        )}

        {messages.map((m, index) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[90%] sm:max-w-[80%] rounded-2xl p-4 ${
              m.role === 'user' 
                ? 'bg-blue-600 text-white shadow-md' 
                : 'bg-gray-100 text-gray-800 shadow-sm'
            }`}>
              <div className="font-bold text-xs mb-1 uppercase tracking-wider opacity-70">
                {m.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="whitespace-pre-wrap break-words">
                {m.content}
              </div>
              
              {/* Render Table if available in the data for this message */}
              {m.role === 'assistant' && (
                <MessageData index={index} messages={messages} data={data} />
              )}
            </div>
          </div>
        ))}
        {isLoading && messages[messages.length - 1]?.role === 'user' && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl p-4 shadow-sm">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-.3s]"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-.5s]"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input */}
      <footer className="p-4 border-t border-gray-200 bg-white">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-2">
          <input
            className="flex-1 p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            value={input}
            placeholder="Type your message..."
            onChange={handleInputChange}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}

function MessageData({ index, messages, data }: { index: number, messages: any[], data: any[] | undefined }) {
  if (!data) return null;

  // In Vercel AI SDK useChat, 'data' contains all data sent so far.
  // We need to find the data that corresponds to this assistant message.
  // A simple heuristic for this implementation: 
  // If this is the last assistant message, show the last table in data.
  
  // Find all assistant messages up to this index
  const assistantMessages = messages.filter((m, i) => m.role === 'assistant' && i <= index);
  const assistantIndex = assistantMessages.length - 1;
  
  // Find all tables in data
  const tables = data.filter(d => d && d.type === 'table');
  
  // If we have a table for this assistant message
  const tableData = tables[assistantIndex];
  
  if (!tableData) return null;

  return <InconvoTable table={tableData.table} />;
}

function InconvoTable({ table }: { table: { head: string[], body: string[][] } }) {
  if (!table || !table.head || !table.body) return null;

  return (
    <div className="mt-4 overflow-hidden border border-gray-300 rounded-lg bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-300">
          <thead className="bg-gray-50">
            <tr>
              {table.head.map((header, i) => (
                <th key={i} className="px-4 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider border-b border-gray-300">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {table.body.map((row, i) => (
              <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                {row.map((cell, j) => (
                  <td key={j} className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
