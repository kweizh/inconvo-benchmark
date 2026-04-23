# Implement Multiple Context Filters in Inconvo Semantic Model

## Background
Inconvo allows you to scope data for multi-tenant applications using context filters. You need to configure a semantic model to enforce authorization rules based on the user's context.

## Requirements
- Update the `inconvo.yaml` semantic model located in `/home/user/project`.
- Add context filters to the `orders` table to restrict data access based on two conditions simultaneously.
- The queries must be restricted to records where the `store_id` matches the `context.store_id`, AND the `region_id` matches the `context.region_id`.

## Implementation Guide
1. Open `/home/user/project/inconvo.yaml`.
2. Locate the `orders` table definition.
3. Add a context filter configuration that applies both the `store_id` and `region_id` conditions. According to Inconvo's multi-tenant setup, context filters use the `context` object.

## Constraints
- Project path: /home/user/project
- The file to modify is `/home/user/project/inconvo.yaml`.
