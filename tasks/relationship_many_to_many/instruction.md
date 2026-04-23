# Configure a Many-to-Many Relationship

## Background
You are building a semantic model for an e-commerce database using Inconvo. You have `orders`, `products`, and a junction table `line_items`.

## Requirements
Configure the relationships in the semantic model to support a many-to-many relationship between `orders` and `products` through `line_items`. This will allow the agent to answer questions like "What products were in order #123?".

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. In the `relations` section, define two relationships:
   - `order_to_line_item`: joining `orders.id` (left) to `line_items.order_id` (right).
   - `line_item_to_product`: joining `line_items.product_id` (left) to `products.id` (right).

## Constraints
- Project path: /home/user/myproject
- The relationships must be named exactly `order_to_line_item` and `line_item_to_product`.
- Do not modify the existing table definitions.