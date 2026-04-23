# Configure Advanced Synonyms in Inconvo Semantic Model

## Background
You have an Inconvo project initialized at `/home/user/project`. The semantic model is defined in `inconvo.yaml`. To improve the natural language understanding of your agent, you need to add custom synonyms to specific fields so that users can query the data using different terminology.

## Requirements
- Update the `inconvo.yaml` file in `/home/user/project`.
- Add the synonyms `revenue` and `gross_sales` to the `total_amount` field in the `orders` table.
- Add the synonym `client_name` to the `name` field in the `customers` table.

## Implementation Guide
1. Open `/home/user/project/inconvo.yaml`.
2. Locate the `orders` table and its `total_amount` field.
3. Add a `synonyms` key (as a list of strings) to the `total_amount` field containing `revenue` and `gross_sales`.
4. Locate the `customers` table and its `name` field.
5. Add a `synonyms` key to the `name` field containing `client_name`.

## Constraints
- Project path: /home/user/project
- The `inconvo.yaml` file must be valid YAML.
- Do not modify any other tables or fields.

## Integrations
- None