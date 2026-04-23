# Metric Definition: Gross Margin

## Background
You have an initialized Inconvo project at `/home/user/inconvo-project` connected to a PostgreSQL database.
The database has a table `sales` with columns `id`, `revenue`, and `cost`.
Currently, there is no column for the gross margin.

## Requirements
Update the semantic model `inconvo.yaml` to define a calculated measure named `gross_margin` on the `sales` table.
It should be calculated as `revenue - cost`.
Set the unit to `USD`.

## Implementation
1. Modify `/home/user/inconvo-project/inconvo.yaml`.
2. Ensure the `sales` table has the `gross_margin` computed column defined with the correct expression and unit.

## Constraints
- **Project path**: `/home/user/inconvo-project`