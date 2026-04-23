# Handle Inconvo Conversation Errors

## Background
You are integrating the Inconvo Data Agent into a Node.js application. When creating a conversation, passing an invalid `userContext` will result in a `BadRequestError`. You need to write a script that attempts to create a conversation and properly catches this specific error.

## Requirements
- Initialize a Node.js project in `/home/user/inconvo-project`.
- Install `@inconvoai/node`.
- Create a script `index.js` that initializes the `Inconvo` client using `process.env.INCONVO_API_KEY`.
- Call `inconvo.agents.conversations.create(process.env.INCONVO_AGENT_ID, { userIdentifier: "test-user", userContext: { invalidKey: "value" } })`.
- Wrap the call in a try-catch block. If the error message includes "Invalid userContext", write the string `Context Error Handled` to `/home/user/inconvo-project/output.log`.
- If it's a different error, it should be thrown.

## Constraints
- Project path: `/home/user/inconvo-project`
- Log file: `/home/user/inconvo-project/output.log`
- Use ESM (ECMAScript Modules) or CommonJS, but ensure it runs with `node index.js`.