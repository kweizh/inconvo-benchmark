Once the semantic model is defined, developers interact with Inconvo through its SDK to create secure chat sessions. The SDK handles sending natural language and receiving structured, validated query plans.

You need to write a standalone Node.js script using the `@inconvoai/node` SDK. The script must initialize the Inconvo client, create a new conversation with a context object containing `organisation_id: 123`, send the message "What was my revenue last month?", and `console.log` the structured response.

**Constraints:**
- You must authenticate the client using the `INCONVO_API_KEY` environment variable.
- Must use TypeScript or modern ESModules syntax.
- The script must successfully await the response from the `conversations.responses.create` API method.