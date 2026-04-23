# Multi-tenant Context Filter in Inconvo

## Background
You are building a multi-tenant e-commerce platform using Inconvo. You need to ensure that when a user asks questions about orders, they only see data for their specific store.

## Requirements
- Configure the `inconvo.yaml` semantic model to include a context filter on the `orders` table.
- The context filter must restrict queries so that `orders.store_id` equals `userContext.store_id`.

## Implementation
1. Modify the `/home/user/myproject/inconvo.yaml` file.
2. Under the `orders` table definition, add a `context_filter` property with the exact value `orders.store_id = userContext.store_id`.

## Constraints
- Project path: /home/user/myproject
- The `inconvo.yaml` file already exists with some basic definitions.