# Vercel AI SDK Integration with Inconvo

## Background
You need to build a streaming chat interface using the Vercel AI SDK and `@inconvoai/vercel-ai-sdk` that renders structured data responses from an Inconvo agent.

## Requirements
- Build a simple Next.js application that provides a chat interface.
- The chat interface should use `useChat` from `ai` (Vercel AI SDK).
- When the agent responds with a `table` data type, render a formatted data grid using a simple HTML `<table>` element.
- The API route should use `@inconvoai/vercel-ai-sdk` to connect to a local Inconvo dev server.

## Implementation Guide
1. Initialize a Next.js project in `/home/user/myproject` (if not already done) and install `ai`, `@ai-sdk/openai`, `@inconvoai/node`, and `@inconvoai/vercel-ai-sdk`.
2. Create an API route `app/api/chat/route.ts` that handles POST requests using the Vercel AI SDK and integrates the Inconvo agent.
3. Create a React component in `app/page.tsx` that uses `useChat`.
4. Ensure that the chat UI correctly parses and renders `table` responses from the assistant.

## Constraints
- Project path: /home/user/myproject
- Start command: npm run build && npm start
- Port: 3000
- The local Inconvo dev server is assumed to be running on port 8000 (mocked or actual).

## Integrations
- None