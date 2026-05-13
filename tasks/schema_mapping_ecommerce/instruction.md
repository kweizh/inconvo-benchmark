# Inconvo Semantic Model for E-commerce

## Background
Inconvo uses a Semantic Layer (`inconvo.yaml`) to map natural language questions into structured query plans. You need to create a semantic model for an e-commerce database with three tables: `orders`, `products`, and `users`.

## Requirements
- Create an `inconvo.yaml` file in the project directory.
- Define three tables: `orders`, `products`, and `users`.
- The `orders` table must be `Queryable`. It should have `id` (state: On), `total_amount` (state: On, type: measure), and `user_id` (state: On).
- The `products` table must be `Queryable`. It should have `id` (state: On), `name` (state: On), and `price` (state: On, type: measure).
- The `users` table must be `Joinable`. It should have `id` (state: On) and `email` (state: On).
- Define relations:
  - `order_to_user`: left `orders.user_id`, right `users.id`.

## Implementation Guide
1. Navigate to `/home/user/ecommerce-agent`.
2. Create the `inconvo.yaml` file with the required tables and fields.
3. Make sure the syntax matches the Inconvo schema format.

## Constraints
- Project path: /home/user/ecommerce-agent
