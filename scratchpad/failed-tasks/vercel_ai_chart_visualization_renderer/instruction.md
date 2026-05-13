# Inconvo Chart Visualization Renderer with Vercel AI SDK

## Background
Inconvo's Vercel AI SDK integration (`@inconvoai/vercel-ai-sdk`) exposes a data agent as a tool that returns structured outputs to the Vercel AI SDK chat stream. When the agent decides the best answer is a chart, the tool output has the shape:

```ts
{ type: "chart", data: { type: "bar" | "line", x: string[], y: number[], xLabel?: string, yLabel?: string } }
```

A partially-built Next.js application is provided at `/home/user/app`. The scaffold already wires `@inconvoai/vercel-ai-sdk` into `app/api/chat/route.ts` and renders the chat UI in `app/page.tsx` using `useChat` from `@ai-sdk/react`. It also contains a placeholder `app/components/inconvo/InconvoChart.tsx` that currently just returns `null`. The `recharts` package is already installed in `node_modules`.

Your job is to implement the chart-rendering component and wire it into the chat UI so the user sees an actual SVG chart whenever the Inconvo agent returns a chart tool output.

## Requirements
1. Implement `app/components/inconvo/InconvoChart.tsx`:
   - Default-export a React component named `InconvoChart`.
   - Accept a single prop `data` with shape `{ type: "bar" | "line", x: string[], y: number[], xLabel?: string, yLabel?: string }`.
   - When `data.type === "bar"` it must render a Recharts `<BarChart>` with a `<Bar>` series. For any other `type` you may fall back to a `<BarChart>` as well.
   - Wrap the chart in a `<div data-testid="inconvo-chart">` element.
   - The chart must produce an `<svg>` element (Recharts renders SVG by default).
   - Combine `x` and `y` into an array of objects (for example `data.x.map((label, i) => ({ name: label, value: data.y[i] }))`) and pass that array to `<BarChart>`. Include `<XAxis dataKey="name" />` and `<Bar dataKey="value" fill="#8884d8" />`.
   - Start the file with `"use client"`.
2. Update `app/page.tsx` (or `app/components/inconvo/InconvoToolResult.tsx` if already wired) so that when an Inconvo tool result has `output.type === "chart"`, it renders `<InconvoChart data={output.data} />`.
3. The project must build (`npm run build`) and serve (`npm start`) successfully on port 3000.

## Implementation Guide
1. Open `/home/user/app/app/components/inconvo/InconvoChart.tsx` and replace the placeholder with a Recharts-based renderer. Import `BarChart`, `Bar`, `XAxis`, `YAxis`, `CartesianGrid`, `Tooltip`, and `ResponsiveContainer` from `recharts`.
2. Map the `{ x: [...], y: [...] }` input shape onto an array of `{ name, value }` objects.
3. Wrap the chart inside a `<div data-testid="inconvo-chart" style={{ width: "100%", height: 320 }}>`.
4. Ensure the existing chat UI delegates to `InconvoChart` when the Inconvo tool returns a `chart` output.
5. Run `npm run build` to confirm there are no TypeScript/build errors.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run build && npm start`
- Port: `3000`
- Environment variables already set: `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, `INCONVO_DB_URL`, `OPENAI_API_KEY`. Use them as-is — never mock.
- `recharts` is already installed in `node_modules`; do NOT add or install new dependencies.

## Integrations
- None
