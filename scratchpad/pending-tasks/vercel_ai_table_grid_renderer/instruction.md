# Inconvo Table Grid Renderer with Vercel AI SDK

## Background
Inconvo provides an integration with the Vercel AI SDK via the `@inconvoai/vercel-ai-sdk` package. When the data agent returns a structured `table` output from a tool call, the React frontend must render it as a styled, interactive data grid with sortable columns.

You are provided with a partially built Next.js 15 application (App Router, TypeScript, Tailwind) at `/home/user/app`. The following are already in place:
- `app/api/chat/route.ts` configured with `inconvoDataAgent` from `@inconvoai/vercel-ai-sdk` and an OpenAI model.
- `app/page.tsx` with a chat UI using the `useChat` hook from `@ai-sdk/react`.
- A placeholder component file at `app/components/inconvo/InconvoTableGrid.tsx` that currently just returns `null`.
- `package.json` already declares `@inconvoai/vercel-ai-sdk`, `@inconvoai/node`, `ai`, `@ai-sdk/react`, `@ai-sdk/openai`, `next`, `react`. `node_modules` is pre-installed.

## Requirements
1. Implement the `InconvoTableGrid` component in `app/components/inconvo/InconvoTableGrid.tsx`:
   - It must accept a prop `data` whose shape is `{ columns: string[]; rows: any[][] }` (this matches the `table` output produced by Inconvo tool calls in this scaffold).
   - It must render an HTML `<table>` element with `data-testid="inconvo-table-grid"`.
   - It must render a `<thead>` containing one `<th>` per column. Each `<th>` must be clickable (`onClick`) to toggle sort order across three states: unsorted -> ascending -> descending -> unsorted. The current sort state for a column must be visible to assistive tech via the `aria-sort` attribute (`"none"`, `"ascending"`, or `"descending"`) and visible to the user via an arrow indicator (e.g. `"▲"` / `"▼"`) next to the column name.
   - It must render a `<tbody>` containing one `<tr>` per row, with one `<td>` per cell. When a column is sorted, the rows displayed in `<tbody>` must be sorted accordingly. Sorting must work for both string and number values.
2. Update `app/page.tsx` to import and render `InconvoTableGrid` whenever a tool result has `output.type === "table"`. For other Inconvo output types (text/chart) or non-tool parts, keep the existing rendering behavior. Pass the table's `columns` and `rows` into `InconvoTableGrid` via the `data` prop.
3. The project must build with `npm run build` and serve with `npm start` on port 3000.

## Implementation Guide
1. `cd /home/user/app`
2. Open `app/components/inconvo/InconvoTableGrid.tsx` and replace the placeholder body with a client component (`"use client"`) that:
   - Uses `useState` to track which column index is currently sorted and the sort direction.
   - Computes a derived `sortedRows` based on the current sort state.
   - Renders the `<table>`, `<thead>`, `<tbody>` structure described in the Requirements.
3. Open `app/page.tsx` and modify the existing tool-output branch so that when the Inconvo tool output has `type === "table"`, the page renders `<InconvoTableGrid data={{ columns: output.columns, rows: output.rows }} />`.
4. Verify the build succeeds: `npm run build`.
5. Start the server: `npm start` (port 3000).

## Constraints
- Project path: /home/user/app
- Start command: npm run build && npm start
- Port: 3000
- Environment Variables: `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, `INCONVO_DB_URL`, and `OPENAI_API_KEY` are set in the environment.
- Do NOT mock any dependencies; the chat route must call the real Inconvo data agent.

## Integrations
- Inconvo (Vercel AI SDK)
- OpenAI (for the chat model used by the Vercel AI SDK route)
