'use client';

import { useChat } from 'ai';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat();

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Header */}
      <header className="sticky top-0 z-10 flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200">
        <h1 className="text-xl font-semibold text-gray-800">Inconvo Chat</h1>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {messages.length === 0 && (
            <div className="text-center py-20 text-gray-500">
              <p className="text-lg">Welcome! Ask me anything about your data.</p>
            </div>
          )}

          {messages.map((m) => (
            <div
              key={m.id}
              className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`flex flex-col gap-2 max-w-[90%] sm:max-w-[80%] ${
                  m.role === 'user' ? 'items-end' : 'items-start'
                }`}
              >
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {m.role === 'user' ? 'You' : 'Assistant'}
                  </span>
                </div>
                
                <div
                  className={`rounded-2xl px-4 py-3 shadow-sm ${
                    m.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <div className="whitespace-pre-wrap leading-relaxed">
                    {m.content}
                  </div>
                </div>

                {/* Render Table if present */}
                {m.role === 'assistant' && renderExtraContent(m)}
              </div>
            </div>
          ))}

          {isLoading && messages[messages.length - 1]?.role !== 'assistant' && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl px-4 py-3 shadow-sm">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Input Area */}
      <footer className="sticky bottom-0 z-10 bg-white border-t border-gray-200 p-6">
        <form
          onSubmit={handleSubmit}
          className="max-w-4xl mx-auto flex gap-4"
        >
          <input
            className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm"
            value={input}
            placeholder="Type your message..."
            onChange={handleInputChange}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm"
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}

function renderExtraContent(message: any) {
  const elements: React.ReactNode[] = [];

  // 1. Check tool invocations for table
  if (message.toolInvocations) {
    message.toolInvocations.forEach((toolInvocation: any) => {
      const { toolCallId, state, result, toolName } = toolInvocation;
      if (state === 'result' && result) {
        // Handle common Inconvo table patterns
        if (result.type === 'table' && result.data) {
          elements.push(<InconvoTable key={toolCallId} data={result.data} />);
        } else if (result.columns && result.rows) {
          elements.push(<InconvoTable key={toolCallId} data={result} />);
        }
      }
    });
  }

  // 2. Check content for embedded JSON table
  try {
    if (message.content.includes('"type":"table"') || (message.content.includes('"columns"') && message.content.includes('"rows"'))) {
      const match = message.content.match(/\{.*"type"\s*:\s*"table".*\}|\{.*"columns"\s*:.*"rows"\s*:.*\}/s);
      if (match) {
        const potentialJson = match[0];
        const data = JSON.parse(potentialJson);
        const tableData = data.type === 'table' ? data.data : data;
        if (tableData && tableData.columns && tableData.rows) {
          elements.push(<InconvoTable key={`content-table-${message.id}`} data={tableData} />);
        }
      }
    }
  } catch (e) {
    // Ignore parse errors
  }

  return elements.length > 0 ? <div className="w-full mt-4 space-y-4">{elements}</div> : null;
}

function InconvoTable({ data }: { data: { columns: string[], rows: any[][] } }) {
  if (!data || !data.columns || !data.rows) return null;

  return (
    <div className="w-full overflow-hidden border border-gray-200 rounded-xl shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {data.columns.map((column, i) => (
                <th
                  key={i}
                  scope="col"
                  className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.rows.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50 transition-colors">
                {row.map((cell, cellIndex) => (
                  <td
                    key={cellIndex}
                    className="px-4 py-3 whitespace-nowrap text-sm text-gray-700"
                  >
                    {renderCell(cell)}
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

function renderCell(cell: any) {
  if (cell === null || cell === undefined) return <span className="text-gray-400 italic">null</span>;
  if (typeof cell === 'boolean') return cell ? 'Yes' : 'No';
  if (typeof cell === 'object') return JSON.stringify(cell);
  return String(cell);
}
