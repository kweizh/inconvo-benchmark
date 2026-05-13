# Configure Many-to-One Relationship in Inconvo

## Background
You have an Inconvo project set up at `/home/user/inconvo-app`. The semantic model is defined in `inconvo.yaml`, which currently contains `line_items` and `products` tables. You need to configure a many-to-one relationship between `line_items` and `products` so the agent can correctly join them.

## Requirements
- Define a relationship named `line_item_to_product` in `inconvo.yaml`.
- The relationship must map `line_items.product_id` to `products.id`.

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml`.
2. Add a `relations` section if it doesn't exist.
3. Add a relation named `line_item_to_product` with `left` pointing to `line_items.product_id` and `right` pointing to `products.id`.

## Constraints
- Project path: /home/user/inconvo-app