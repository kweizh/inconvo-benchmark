"use client";

import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";

function isInconvoTool(toolName: string): boolean {
  return (
    toolName.includes("DataAgent") ||
    toolName.includes("DataSummary") ||
    toolName === "getDataAgentConnectedDataSummary" ||
    toolName === "startDataAgentConversation" ||
    toolName === "messageDataAgent"
  );
}

export default function Home() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: "/api/chat" }),
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const text = input;
    setInput("");
    await sendMessage({ text });
  };

  return (
    <main className="flex flex-col items-center justify-between min-h-screen p-8 bg-gray-50">
      <div className="w-full max-w-2xl flex flex-col gap-4">
        <h1 className="text-2xl font-bold text-gray-800">Inconvo Data Agent</h1>

        <div className="flex flex-col gap-4 flex-1 overflow-y-auto min-h-[400px] bg-white rounded-lg shadow p-4">
          {messages.length === 0 && (
            <p className="text-gray-400 text-center mt-8">
              Ask a question about your data to get started.
            </p>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-800"
                }`}
              >
                {message.parts.map((part, partIndex) => {
                  if (part.type === "text") {
                    return (
                      <p key={partIndex} className="whitespace-pre-wrap">
                        {part.text}
                      </p>
                    );
                  }

                  if (
                    part.type === "dynamic-tool" &&
                    isInconvoTool(part.toolName) &&
                    part.state === "output-available"
                  ) {
                    return (
                      <div key={partIndex} data-testid="inconvo-result">
                        Data Visualization Available
                      </div>
                    );
                  }

                  return null;
                })}
              </div>
            </div>
          ))}

          {status === "streaming" && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2">
                <span className="animate-pulse">Thinking...</span>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your data..."
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={status === "streaming"}
            className="rounded-lg bg-blue-600 text-white px-6 py-2 font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
      </div>
    </main>
  );
}
