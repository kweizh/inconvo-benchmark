"use client";

import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from "react";
import {
  AbstractChat,
  DefaultChatTransport,
  UIMessage,
  ChatState,
  ChatStatus,
} from "ai";

// ---------------------------------------------------------------------------
// Minimal useChat implementation built on AbstractChat + DefaultChatTransport
// ---------------------------------------------------------------------------

class ReactChat extends AbstractChat<UIMessage> {
  private subscribers = new Set<() => void>();

  constructor(api: string) {
    const transport = new DefaultChatTransport({ api });

    const mutableState = {
      messages: [] as UIMessage[],
      status: "ready" as ChatStatus,
      error: undefined as Error | undefined,
    };

    const subscribers = new Set<() => void>();

    const notify = () => {
      subscribers.forEach((sub) => sub());
    };

    const state: ChatState<UIMessage> = {
      get status() {
        return mutableState.status;
      },
      get error() {
        return mutableState.error;
      },
      get messages() {
        return mutableState.messages;
      },
      pushMessage(message) {
        mutableState.messages = [...mutableState.messages, message];
        notify();
      },
      popMessage() {
        mutableState.messages = mutableState.messages.slice(0, -1);
        notify();
      },
      replaceMessage(index, message) {
        mutableState.messages = [
          ...mutableState.messages.slice(0, index),
          message,
          ...mutableState.messages.slice(index + 1),
        ];
        notify();
      },
      snapshot<T>(thing: T): T {
        return thing;
      },
    };

    super({ transport, state });

    this.subscribers = subscribers;

    // Intercept setStatus so we notify React when status/error changes
    const origSetStatus = (this as unknown as { setStatus: (args: { status: ChatStatus; error?: Error }) => void }).setStatus.bind(this);
    (this as unknown as { setStatus: (args: { status: ChatStatus; error?: Error }) => void }).setStatus = (args) => {
      mutableState.status = args.status;
      mutableState.error = args.error;
      origSetStatus(args);
      notify();
    };
  }

  subscribe(callback: () => void) {
    this.subscribers.add(callback);
    return () => {
      this.subscribers.delete(callback);
    };
  }

  getSnapshot() {
    return {
      messages: this.messages,
      status: this.status,
      error: this.error,
    };
  }
}

function useChat(api: string = "/api/chat") {
  const chatRef = useRef<ReactChat | null>(null);
  if (!chatRef.current) {
    chatRef.current = new ReactChat(api);
  }
  const chat = chatRef.current;

  const snapshot = useSyncExternalStore(
    useCallback((cb) => chat.subscribe(cb), [chat]),
    useCallback(() => chat.getSnapshot(), [chat]),
    useCallback(() => chat.getSnapshot(), [chat]),
  );

  const [input, setInput] = useState("");

  const handleSubmit = useCallback(
    async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const text = input.trim();
      if (!text) return;
      setInput("");
      await chat.sendMessage({ text });
    },
    [chat, input],
  );

  return {
    messages: snapshot.messages,
    status: snapshot.status,
    error: snapshot.error,
    input,
    setInput,
    handleSubmit,
  };
}

// ---------------------------------------------------------------------------
// Table renderer
// ---------------------------------------------------------------------------

interface InconvoTable {
  head: string[];
  body: string[][];
}

interface InconvoResponse {
  id?: string;
  conversationId?: string;
  message?: string;
  type: "text" | "chart" | "table";
  table?: InconvoTable;
}

function DataTable({ table }: { table: InconvoTable }) {
  return (
    <div className="overflow-x-auto my-2">
      <table className="min-w-full border border-gray-300 text-sm">
        <thead className="bg-gray-100">
          <tr>
            {table.head.map((col, i) => (
              <th
                key={i}
                className="border border-gray-300 px-3 py-2 text-left font-semibold text-gray-700"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {table.body.map((row, rowIdx) => (
            <tr
              key={rowIdx}
              className={rowIdx % 2 === 0 ? "bg-white" : "bg-gray-50"}
            >
              {row.map((cell, cellIdx) => (
                <td
                  key={cellIdx}
                  className="border border-gray-300 px-3 py-2 text-gray-800"
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

// ---------------------------------------------------------------------------
// Message part renderer
// ---------------------------------------------------------------------------

function tryParseInconvoResponse(text: string): InconvoResponse | null {
  try {
    const parsed = JSON.parse(text);
    if (parsed && typeof parsed === "object" && "type" in parsed) {
      return parsed as InconvoResponse;
    }
  } catch {
    // not JSON – that's fine
  }
  return null;
}

function MessageContent({ message }: { message: UIMessage }) {
  const parts = message.parts ?? [];

  return (
    <div className="space-y-1">
      {parts.map((part, i) => {
        if (part.type === "text") {
          const parsed = tryParseInconvoResponse(part.text);
          if (parsed?.type === "table" && parsed.table) {
            return <DataTable key={i} table={parsed.table} />;
          }
          return (
            <p key={i} className="whitespace-pre-wrap">
              {part.text}
            </p>
          );
        }

        if (part.type === "dynamic-tool" && part.state === "output-available") {
          const output = part.output as InconvoResponse | string | undefined;
          if (output && typeof output === "object" && output.type === "table" && output.table) {
            return <DataTable key={i} table={output.table} />;
          }
          if (output && typeof output === "string") {
            const parsed = tryParseInconvoResponse(output);
            if (parsed?.type === "table" && parsed.table) {
              return <DataTable key={i} table={parsed.table} />;
            }
          }
        }

        return null;
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function Home() {
  const { messages, status, error, input, setInput, handleSubmit } = useChat("/api/chat");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const isLoading = status === "submitted" || status === "streaming";

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <h1 className="text-xl font-semibold text-gray-900">Inconvo Data Chat</h1>
        <p className="text-sm text-gray-500">Ask questions about your data</p>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">👋 Ask a question about your data</p>
          </div>
        )}

        {messages.map((message) => {
          const isUser = message.role === "user";
          return (
            <div
              key={message.id}
              className={`flex ${isUser ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-3xl rounded-2xl px-4 py-3 shadow-sm ${
                  isUser
                    ? "bg-blue-600 text-white"
                    : "bg-white border border-gray-200 text-gray-900"
                }`}
              >
                <div className="text-xs font-medium mb-1 opacity-60">
                  {isUser ? "You" : "Assistant"}
                </div>
                <MessageContent message={message} />
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
              <div className="flex gap-1 items-center">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="text-red-600 text-sm text-center">
            Error: {error.message}
          </div>
        )}

        <div ref={bottomRef} />
      </main>

      {/* Input */}
      <footer className="bg-white border-t border-gray-200 px-4 py-4">
        <form onSubmit={handleSubmit} className="flex gap-2 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your data…"
            disabled={isLoading}
            className="flex-1 rounded-xl border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="rounded-xl bg-blue-600 text-white px-5 py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}
