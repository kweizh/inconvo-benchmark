# Inconvo Next.js Vercel AI SDK Integration

## Background
You need to build a Next.js application that integrates with Inconvo using the Vercel AI SDK to create an interactive data agent chat interface.

## Requirements
- Initialize a Next.js application (App Router, TypeScript, Tailwind CSS, no `src` directory) in `/home/user/app`.
- Install the required packages: `ai`, `@ai-sdk/react`, and `@inconvoai/vercel-ai-sdk`.
- Create a backend API route at `app/api/chat/route.ts` that uses `streamText` from `ai` and `inconvoDataAgent` from `@inconvoai/vercel-ai-sdk`.
- The API route must configure the agent with `process.env.INCONVO_AGENT_ID`, a `userIdentifier` of `"user-123"`, and a `userContext` with `organisationId: 1`.
- Create a frontend chat interface in `app/page.tsx` using the `useChat` hook from `@ai-sdk/react`.
- The UI must include an input field with the placeholder "Ask about your data..." and display the conversation messages.
- For tool calls, if the tool is an Inconvo tool and its state is `output-available`, the UI should render a generic `<div data-testid="inconvo-result">Data Visualization Available</div>`.

## Implementation Guide
1. Run `npx create-next-app@latest /home/user/app --ts --tailwind --eslint --app --no-src-dir --import-alias "@/*"` to create the project.
2. Add the necessary dependencies.
3. Implement the `POST` handler in `app/api/chat/route.ts` to convert messages and call `streamText` with the `inconvoDataAgent` tool, returning `result.toUIMessageStreamResponse()`.
4. Implement the chat UI in `app/page.tsx` by iterating over `messages` from `useChat` and rendering user/AI text, as well as tool results.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run build && npm start`
- Port: `3000`
- Environment: Use Node.js v24.
- Note: Do not configure real API keys, the verifier will only check the static UI and code implementation.

## Integrations
- None