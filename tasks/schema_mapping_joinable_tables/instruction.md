# Configure Customers Table as Joinable

## Background
Inconvo uses a semantic model defined in `inconvo.yaml` to map natural language to data. You have an existing Inconvo project where the `customers` table is currently configured as `Queryable`.

## Requirements
- Update the `inconvo.yaml` file to configure the `customers` table as `Joinable` only, not `Queryable` directly.
- Run the `index.js` script to generate a `response.json` file verifying the configuration.

## Implementation Guide
1. Open the `inconvo.yaml` file located in `/home/user/inconvo-app`.
2. Locate the `customers` table definition.
3. Change its `state` from `Queryable` to `Joinable`.
4. Run `node index.js` in the project directory. This will query the agent and save the result to `response.json`.

## Constraints
- Project path: /home/user/inconvo-app

## Integrations
- None