# Define a Calculated Measure in Inconvo Semantic Model

## Background
You are working on an Inconvo project located at `/home/user/myproject`. The project already has a basic semantic model defined in `inconvo.yaml`. You need to add a new calculated measure to the `orders` table to track the gross margin.

## Requirements
- Update the `inconvo.yaml` file in the project directory.
- In the `orders` table, add a new field named `gross_margin`.
- The `gross_margin` field should have its state set to `On`.
- The `gross_margin` field should have its type set to `measure`.
- The `gross_margin` field should include a calculation or sql definition representing `revenue - cost` (e.g., `sql: revenue - cost`).

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Locate the `orders` table under `tables`.
3. Add the `gross_margin` field to the `fields` section of the `orders` table with the required attributes.

## Constraints
- Project path: `/home/user/myproject`
- The `inconvo.yaml` file must remain valid YAML.