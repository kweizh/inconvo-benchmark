# Inconvo Streaming UI with Vercel AI SDK

## Background
Inconvo provides a middleware for building chat-with-data agents. You can use `@inconvoai/vercel-ai-sdk` to stream responses to a React frontend using the Vercel AI SDK.

## Requirements
- You are provided with a Next.js application in `/home/user/app`.
- Implement an API route at `app/api/chat/route.ts` that uses `@inconvoai/vercel-ai-sdk` and `@inconvoai/node` to handle chat messages and stream the response from Inconvo.
- Implement the main UI in `app/page.tsx` using the `useChat` hook from the `ai` package.
- When the agent returns a `table` response, render it as a formatted HTML data grid (`<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`).
- The table should display the data correctly based on the streamed Inconvo table response structure.

## Implementation Guide
1. Use `@inconvoai/node` to initialize the Inconvo client in the API route.
2. Use `@inconvoai/vercel-ai-sdk` to stream the response back to the client.
3. In `app/page.tsx`, use `useChat` to manage the chat state.
4. Render user messages as text.
5. For assistant messages, if the content or tool invocation represents a table, render it as an HTML `<table>`.

## Constraints
- Project path: /home/user/app
- Start command: npm run build && npm start
- Port: 3000
- Environment Variables: `INCONVO_API_KEY` and `INCONVO_AGENT_ID` are set in the environment.

## Integrations
- None