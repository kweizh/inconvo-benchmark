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
LABEL Description="Next.js + Inconvo Vercel AI SDK scaffold with a placeholder InconvoTableGrid component to be implemented."

# Scaffold the Next.js 15 application at /home/user/app
RUN cd /home/user && \
    npx --yes create-next-app@15 app \
        --typescript --eslint --app --no-src-dir \
        --import-alias "@/*" --use-npm --tailwind --turbopack=false --yes && \
    cd app && \
    npm install --legacy-peer-deps @inconvoai/node @inconvoai/vercel-ai-sdk ai @ai-sdk/react @ai-sdk/openai

# Relax ESLint and TypeScript strictness during `next build` so that the agent's
# implementation isn't blocked by stylistic lint rules (e.g. no-explicit-any).
RUN cat >/home/user/app/next.config.ts <<'EOF'
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
};

export default nextConfig;
EOF

# Pre-create the placeholder InconvoTableGrid component (returns null — to be implemented by the agent)
RUN mkdir -p /home/user/app/app/components/inconvo && \
    cat >/home/user/app/app/components/inconvo/InconvoTableGrid.tsx <<'EOF'
"use client";

// PLACEHOLDER component. Implement this to render Inconvo `table` outputs
// as a sortable HTML data grid. See the task description for requirements.
//
// Required props:
//   data: { columns: string[]; rows: any[][] }
//
// The rendered <table> must include `data-testid="inconvo-table-grid"`.

export interface InconvoTableGridProps {
  data: {
    columns: string[];
    rows: any[][];
  };
}

export function InconvoTableGrid(_props: InconvoTableGridProps) {
  return null;
}

export default InconvoTableGrid;
EOF

# Pre-create the chat API route using @inconvoai/vercel-ai-sdk
RUN mkdir -p /home/user/app/app/api/chat && \
    cat >/home/user/app/app/api/chat/route.ts <<'EOF'
import { streamText, convertToModelMessages, stepCountIs } from "ai";
import { inconvoDataAgent } from "@inconvoai/vercel-ai-sdk";
import { openai } from "@ai-sdk/openai";

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

# Pre-create the chat page using the useChat hook
RUN cat >/home/user/app/app/page.tsx <<'EOF'
"use client";

import { useChat } from "@ai-sdk/react";
import { useState } from "react";
import { InconvoTableGrid } from "./components/inconvo/InconvoTableGrid";

type InconvoOutput =
  | { type: "text"; text: string }
  | { type: "table"; columns: string[]; rows: any[][] }
  | { type: "chart"; [key: string]: any };

function isInconvoOutput(output: unknown): output is InconvoOutput {
  return (
    typeof output === "object" &&
    output !== null &&
    "type" in output &&
    typeof (output as any).type === "string" &&
    ["text", "table", "chart"].includes((output as any).type)
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
            {message.parts.map((part: any, i: number) => {
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

              if (part.type?.startsWith("tool-") && "state" in part) {
                const isInconvoTool =
                  typeof part.type === "string" &&
                  part.type.includes("DataAgent");

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
                  isInconvoOutput(part.output)
                ) {
                  // TODO (agent): when output.type === "table",
                  // render <InconvoTableGrid data={{ columns, rows }} /> here.
                  return (
                    <pre
                      key={`${message.id}-${i}`}
                      className="text-xs bg-zinc-50 p-2 overflow-auto"
                    >
                      {JSON.stringify(part.output, null, 2)}
                    </pre>
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
          if (!input.trim()) return;
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

# Pre-build the application so `npm run build` is fast at evaluation time
RUN cd /home/user/app && npm run build || true

# Container contents:
#   - Node.js v24 and browser verification dependencies (agent-browser, ffmpeg, ripgrep, libs)
#   - /home/user/app: Next.js 15 app pre-installed with @inconvoai/node,
#     @inconvoai/vercel-ai-sdk, ai, @ai-sdk/react, @ai-sdk/openai.
#   - /home/user/app/app/api/chat/route.ts: chat endpoint using inconvoDataAgent.
#   - /home/user/app/app/page.tsx: chat UI using useChat (renders tool outputs as JSON).
#   - /home/user/app/app/components/inconvo/InconvoTableGrid.tsx: placeholder
#     component returning null — the agent must implement the sortable data grid.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
