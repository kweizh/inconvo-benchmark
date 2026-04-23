# Configure Dimension and Measure Types in Inconvo

## Background
You are working on an Inconvo semantic model for an e-commerce database. The `inconvo.yaml` file defines how the AI agent interacts with your database. Currently, the `orders` table has fields `total_amount` and `created_at` mapped, but their types are not specified.

## Requirements
- Update the `inconvo.yaml` file to explicitly define `total_amount` as a `measure`.
- Update the `inconvo.yaml` file to explicitly define `created_at` as a `dimension`.
- Ensure both fields have their state set to `On`.

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Locate the `orders` table and its `fields`.
3. Modify the `total_amount` field to include `type: measure` and `state: On`.
4. Modify the `created_at` field to include `type: dimension` and `state: On`.

## Constraints
- Project path: /home/user/myproject
- Do not modify other tables or fields.

## Integrations
- None