'use client';

import { useState } from 'react';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

export default function Home() {
  const [input, setInput] = useState('');
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: '/api/chat',
    }),
  });

  const isLoading = status === 'streaming' || status === 'submitted';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const message = input.trim();
    setInput('');
    await sendMessage({ text: message });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-900">Inconvo Chat</h1>
        <p className="text-sm text-gray-600">Chat with your data using AI</p>
      </header>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <p>Start a conversation by typing a message below</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-3xl rounded-lg px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-900 border border-gray-200'
                }`}
              >
                {message.role === 'user' ? (
                  <p className="whitespace-pre-wrap">{message.content}</p>
                ) : (
                  <AssistantMessage message={message} />
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="bg-white border-t border-gray-200 p-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}

function AssistantMessage({ message }: { message: { role: string; content: string | Array<{ type: string; text?: string; data?: unknown }> } }) {
  // Check if the message has data parts
  if (message.content && Array.isArray(message.content)) {
    for (const part of message.content) {
      if (part.type === 'text') {
        return <p className="whitespace-pre-wrap">{part.text}</p>;
      } else if (part.type === 'data') {
        try {
          const data = typeof part.data === 'string' ? JSON.parse(part.data) : part.data;
          
          if (data.type === 'table' && data.table) {
            return <TableComponent table={data.table} />;
          }
          
          if (data.type === 'chart' && data.chart) {
            return (
              <div>
                <p className="mb-2">Chart visualization:</p>
                <div className="bg-gray-100 p-4 rounded">
                  <pre className="text-xs overflow-auto max-h-64">
                    {JSON.stringify(data.chart, null, 2)}
                  </pre>
                </div>
              </div>
            );
          }
        } catch {
          // If parsing fails, continue to next part
        }
      }
    }
  }

  // Fall back to rendering content as text
  const content = typeof message.content === 'string' ? message.content : '';
  
  try {
    // Try to parse the content as JSON
    const parsed = JSON.parse(content);
    
    // Check if it's a table response
    if (parsed.type === 'table' && parsed.table) {
      return <TableComponent table={parsed.table} />;
    }
    
    // Check if it's a chart response
    if (parsed.type === 'chart' && parsed.chart) {
      return (
        <div>
          <p className="mb-2">Chart visualization:</p>
          <div className="bg-gray-100 p-4 rounded">
            <pre className="text-xs overflow-auto max-h-64">
              {JSON.stringify(parsed.chart, null, 2)}
            </pre>
          </div>
        </div>
      );
    }
    
    // If it's not a special type, render as text
    return <p className="whitespace-pre-wrap">{content}</p>;
  } catch {
    // If parsing fails, render as plain text
    return <p className="whitespace-pre-wrap">{content}</p>;
  }
}

function TableComponent({ table }: { table: { head: string[]; body: string[][] } }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {table.head.map((header, index) => (
              <th
                key={index}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {table.body.map((row, rowIndex) => (
            <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              {row.map((cell, cellIndex) => (
                <td
                  key={cellIndex}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                >
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