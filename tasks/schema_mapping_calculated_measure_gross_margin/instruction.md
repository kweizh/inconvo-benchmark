# Define a Calculated Measure in Inconvo

## Background
Inconvo uses a Semantic Layer (`inconvo.yaml`) to map natural language to SQL. You need to define a calculated measure for "Gross Margin" (Revenue - Cost) within the semantic layer.

## Requirements
- You have an Inconvo project located at `/home/user/inconvo-app`.
- The `inconvo.yaml` file contains an `orders` table with `revenue` and `cost` fields.
- Add a new calculated measure named `gross_margin` to the `orders` table.
- The calculated measure should represent Revenue minus Cost.

## Implementation Guide
1. Open `/home/user/inconvo-app/inconvo.yaml`.
2. Locate the `orders` table and its `fields` section.
3. Add a new field `gross_margin` with state `On`, type `measure`, and an appropriate SQL expression (e.g., `sql: "revenue - cost"`).

## Constraints
- Project path: `/home/user/inconvo-app`
- The file to modify is `inconvo.yaml`.

## Integrations
- None