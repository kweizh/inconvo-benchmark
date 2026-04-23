# Configure Column Synonyms in Semantic Model

## Background
Inconvo uses a Semantic Layer (`inconvo.yaml`) to map natural language to SQL. You can define synonyms for columns to ensure the AI agent correctly understands different terms users might use to refer to the same data.

## Requirements
You have an Inconvo project initialized at `/home/user/inconvo-project` with an `orders` table defined in the `inconvo.yaml` semantic model.
Your task is to update the semantic model to add synonyms to the `total_amount` column so that users can query it using the terms "revenue" and "sales".

## Implementation
1. Open the file `/home/user/inconvo-project/inconvo.yaml`.
2. Locate the `orders` table and its `total_amount` field.
3. Add a `synonyms` property to the `total_amount` field containing the list of terms: `["revenue", "sales"]`.

## Constraints
- Project path: `/home/user/inconvo-project`