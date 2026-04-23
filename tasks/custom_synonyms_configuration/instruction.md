# Configure Custom Synonyms in Inconvo

## Background
You have an Inconvo project initialized at `/home/user/myproject`. The project contains a semantic model in `inconvo.yaml` with an `orders` table that has a `total_amount` field. To improve the natural language mapping, we want users to be able to ask for "revenue" or "income" and have the system correctly map it to `total_amount`.

## Requirements
- Update the `inconvo.yaml` file to include synonyms for the `total_amount` field in the `orders` table.
- The synonyms must include both "revenue" and "income".

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Locate the `tables` -> `orders` -> `fields` -> `total_amount` definition.
3. Add a `synonyms` array property to the field configuration containing `"revenue"` and `"income"`.

## Constraints
- Project path: `/home/user/myproject`
- The file to modify is `/home/user/myproject/inconvo.yaml`.
- Do not change any other existing configurations in the file.

## Integrations
- None