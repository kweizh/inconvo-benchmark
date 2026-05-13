# Inconvo Schema Mapping: Synonyms and Hidden Fields

## Background
You have an Inconvo project at `/home/user/inconvo-app`. It contains a semantic model configuration file `inconvo.yaml` for an e-commerce database. You need to hide internal fields and add synonyms to improve the natural language querying experience.

## Requirements
- Edit `inconvo.yaml` in the `/home/user/inconvo-app` directory.
- The `users` table has an `internal_id` field. Change its state to `Off` to hide it from the AI.
- The `products` table has a `title` field. Add synonyms `["name", "item name"]` to it so users can ask about "product name" or "item name".
- The `orders` table has a `total_amount` field. Add a synonym `["revenue"]` to it.

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml`.
2. Locate the `users` table and update the `internal_id` field to have `state: Off`.
3. Locate the `products` table and update the `title` field to include `synonyms: ["name", "item name"]`.
4. Locate the `orders` table and update the `total_amount` field to include `synonyms: ["revenue"]`.

## Constraints
- Project path: `/home/user/inconvo-app`

## Integrations
- None