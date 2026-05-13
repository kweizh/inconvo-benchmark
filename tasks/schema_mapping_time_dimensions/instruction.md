# Configure Time Dimension in Inconvo

## Background
You have an Inconvo project set up at `/home/user/inconvo-app`. The project contains a semantic model configuration file `inconvo.yaml` with an `orders` table. You need to configure the `created_at` field as a time dimension to allow temporal queries, and then run a script to verify the configuration.

## Requirements
- Update the `inconvo.yaml` file in the project directory.
- Locate the `orders` table and its `created_at` field.
- Configure the `created_at` field to be queryable (`state: On`) and explicitly set its type to `dimension`.
- Run `node index.js` to ensure the configuration is valid and can answer a time-based question.

## Constraints
- Project path: `/home/user/inconvo-app`
- File to modify: `/home/user/inconvo-app/inconvo.yaml`

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml`.
2. Find the `tables` section and the `orders` table.
3. In the `fields` section of `orders`, add or update the `created_at` field to have `{ state: On, type: dimension }`.
4. Run `node index.js` to verify the setup.