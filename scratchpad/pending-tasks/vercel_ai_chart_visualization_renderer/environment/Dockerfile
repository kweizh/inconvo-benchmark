FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        ffmpeg ripgrep libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 libxshmfence1 libgbm1 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @getpochi/cli agent-browser && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN agent-browser install || true

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Next.js + Inconvo Vercel AI SDK scaffold with recharts pre-installed and browser verification dependencies for chart rendering tasks."

# Scaffold the Next.js app at /home/user/app and pre-install all required deps.
RUN cd /home/user && \
    npx --yes create-next-app@14 app --typescript --eslint --app --no-src-dir --import-alias "@/*" --use-npm --tailwind --yes && \
    cd app && \
    npm install @inconvoai/node @inconvoai/vercel-ai-sdk @ai-sdk/react @ai-sdk/openai ai recharts

# Pre-populate the partially-built source files so the agent's only job is to
# implement the chart rendering component and wire it into page.tsx.
RUN mkdir -p /home/user/app/app/api/chat /home/user/app/app/components/inconvo

RUN cat >/home/user/app/app/api/chat/route.ts <<'EOF'
import { streamText, convertToModelMessages, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";
import { inconvoDataAgent } from "@inconvoai/vercel-ai-sdk";

export const maxDuration = 60;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai("gpt-4o-mini"),
    system: `When you receive structured data (tables, charts) from tools,
      do NOT recreate or reformat them as markdown tables in your response.
      The tool output will be displayed directly as interactive UI.
      You may provide brief context, insights, or follow-up suggestions,
      but never duplicate the data itself.`,
    messages: await convertToModelMessages(messages),
    tools: {
      ...inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID!,
        userIdentifier: "user-123",
        userContext: {
          organisationId: 1,
        },
      }),
    },
    stopWhen: stepCountIs(5),
  });

  return result.toUIMessageStreamResponse();
}
EOF

RUN cat >/home/user/app/app/components/inconvo/InconvoChart.tsx <<'EOF'
"use client";

// TODO: Implement this component to render Inconvo chart outputs using recharts.
// It receives a `data` prop with shape:
//   { type: "bar" | "line", x: string[], y: number[], xLabel?: string, yLabel?: string }
// and must render an SVG chart wrapped in <div data-testid="inconvo-chart">.

type InconvoChartData = {
  type: "bar" | "line";
  x: string[];
  y: number[];
  xLabel?: string;
  yLabel?: string;
};

export default function InconvoChart(_props: { data: InconvoChartData }) {
  return null;
}
EOF

RUN cat >/home/user/app/app/components/inconvo/InconvoToolResult.tsx <<'EOF'
"use client";

import InconvoChart from "./InconvoChart";

type InconvoOutput =
  | { type: "text"; text: string }
  | { type: "table"; data: { columns: string[]; rows: unknown[][] } }
  | {
      type: "chart";
      data: {
        type: "bar" | "line";
        x: string[];
        y: number[];
        xLabel?: string;
        yLabel?: string;
      };
    };

export function InconvoToolResult({ result }: { result: InconvoOutput }) {
  if (result.type === "text") {
    return <div className="whitespace-pre-wrap">{result.text}</div>;
  }

  if (result.type === "table") {
    return (
      <div className="overflow-x-auto" data-testid="inconvo-table">
        <table className="min-w-full border">
          <thead>
            <tr>
              {result.data.columns.map((c) => (
                <th key={c} className="border px-2 py-1 text-left">
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.data.rows.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <td key={j} className="border px-2 py-1">
                    {String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (result.type === "chart") {
    // The agent must implement InconvoChart so this branch renders a chart.
    return <InconvoChart data={result.data} />;
  }

  return null;
}
EOF

RUN cat >/home/user/app/app/page.tsx <<'EOF'
"use client";

import { useChat } from "@ai-sdk/react";
import { useState } from "react";
import { InconvoToolResult } from "./components/inconvo/InconvoToolResult";

function isInconvoOutput(output: unknown): boolean {
  return (
    typeof output === "object" &&
    output !== null &&
    "type" in output &&
    typeof (output as { type?: unknown }).type === "string" &&
    ["text", "table", "chart"].includes((output as { type: string }).type)
  );
}

export default function Chat() {
  const [input, setInput] = useState("");
  const { messages, sendMessage } = useChat();

  return (
    <div className="flex flex-col w-full max-w-4xl py-24 mx-auto px-4">
      {messages.map((message) => (
        <div key={message.id} className="mb-4">
          <div className="font-semibold mb-1">
            {message.role === "user" ? "User" : "AI"}:
          </div>
          <div>
            {message.parts.map((part, i) => {
              if (part.type === "text") {
                return (
                  <div
                    key={`${message.id}-${i}`}
                    className="whitespace-pre-wrap"
                  >
                    {part.text}
                  </div>
                );
              }

              if (part.type.startsWith("tool-") && "state" in part) {
                const isInconvoTool = part.type.includes("DataAgent");

                if (part.state === "input-available" && isInconvoTool) {
                  return (
                    <div
                      key={`${message.id}-${i}`}
                      className="flex items-center gap-2 p-4 text-sm text-zinc-500"
                    >
                      <div className="animate-spin h-4 w-4 border-2 border-zinc-300 border-t-zinc-600 rounded-full" />
                      <div>Querying your data...</div>
                    </div>
                  );
                }

                if (
                  part.state === "output-available" &&
                  "output" in part &&
                  isInconvoOutput((part as { output: unknown }).output)
                ) {
                  return (
                    <InconvoToolResult
                      key={`${message.id}-${i}`}
                      result={(part as { output: any }).output}
                    />
                  );
                }
              }

              return null;
            })}
          </div>
        </div>
      ))}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (input.trim().length === 0) return;
          sendMessage({ text: input });
          setInput("");
        }}
      >
        <input
          className="fixed bottom-0 w-full max-w-4xl p-2 mb-8 border border-zinc-300 rounded shadow-xl"
          value={input}
          placeholder="Ask about your data..."
          onChange={(e) => setInput(e.currentTarget.value)}
        />
      </form>
    </div>
  );
}
EOF

# Container contents:
#   - Ubuntu 24.04 with Node.js v24, Pochi CLI, agent-browser, and full browser
#     verification dependencies (ffmpeg, ripgrep, X libs).
#   - /home/user/app: Next.js 14 App Router scaffold (TypeScript + Tailwind)
#     with @inconvoai/node, @inconvoai/vercel-ai-sdk, @ai-sdk/react,
#     @ai-sdk/openai, ai, and recharts installed in node_modules.
#   - Pre-existing app/api/chat/route.ts wiring inconvoDataAgent into the
#     Vercel AI SDK streamText route using OPENAI_API_KEY.
#   - Pre-existing app/page.tsx with useChat-based chat UI and the
#     InconvoToolResult dispatcher that delegates "chart" outputs to
#     app/components/inconvo/InconvoChart.tsx (placeholder returning null).
#   - The agent must implement InconvoChart.tsx using recharts.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
