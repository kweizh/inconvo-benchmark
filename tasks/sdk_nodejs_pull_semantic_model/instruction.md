# Pull Inconvo Semantic Model

## Background
You have a Node.js project at `/home/user/inconvo-app` that uses the Inconvo SDK. You need to pull the latest semantic model from your Inconvo Data Agent to your local environment.

## Requirements
- Use the Inconvo CLI to pull the semantic model.
- Ensure the command is executed within the project directory.

## Implementation Guide
1. Change directory to `/home/user/inconvo-app`.
2. Run the Inconvo CLI command to pull the model: `npx inconvo model pull`.

## Constraints
- Project path: `/home/user/inconvo-app`
- The environment variables `INCONVO_API_KEY` and `INCONVO_AGENT_ID` are already available in the environment.
- You must use the `inconvo` CLI via `npx`.