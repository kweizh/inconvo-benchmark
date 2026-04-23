# Inconvo Implementation Report

## Project Structure
- `inconvo.yaml`: Semantic model defining `orders` and `products`.
- `index.js`: Node.js script using `@inconvoai/node` to query the agent.
- `package.json`: Project configuration and dependencies.

## Semantic Model Details
The model includes:
- `orders` model with a `total_amount` measure (sum).
- `products` model with a `name` dimension.
- A `many_to_one` relationship between `orders` and `products` joined on `product_id`.

## Script Logic
The script performs the following:
1. Initializes the `Inconvo` client.
2. Creates a new conversation thread for a specific user.
3. Sends the query "What are my top products?".
4. Extracts the `table` property from the response and saves it to `response.json`.
