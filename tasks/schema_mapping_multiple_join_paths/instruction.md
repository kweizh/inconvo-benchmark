# Explicitly Constrain Join Paths in Inconvo

## Background
Inconvo uses a Semantic Layer (`inconvo.yaml`) to map natural language to SQL. When multiple join paths exist between tables (e.g., an order has both a `buyer_id` and a `seller_id` pointing to a `users` table), the agent may pick the wrong one unless explicitly defined in the YAML.

## Requirements
- You have an Inconvo project at `/home/user/inconvo-app` with an initial `inconvo.yaml`.
- The schema includes `orders` and `users` tables.
- The `orders` table has `buyer_id` and `seller_id` columns, both referencing `users.id`.
- Update `inconvo.yaml` to explicitly define two relationships:
  1. Name: `order_to_buyer`, Left: `orders.buyer_id`, Right: `users.id`
  2. Name: `order_to_seller`, Left: `orders.seller_id`, Right: `users.id`
- Create a Node.js script `index.js` that initializes the `@inconvoai/node` client and saves the client instance to a global variable (for testing purposes, just write a basic script that can be executed without throwing errors). The script must require `@inconvoai/node`.

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml`.
2. Add a `relations` section at the root level if it doesn't exist.
3. Define the `order_to_buyer` and `order_to_seller` relationships as specified.
4. Create `/home/user/inconvo-app/index.js` requiring the SDK.

## Constraints
- Project path: `/home/user/inconvo-app`