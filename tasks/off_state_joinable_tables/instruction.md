# Configure Table States in Inconvo

## Background
Inconvo uses a Semantic Model (`inconvo.yaml`) to map natural language questions into structured query plans. Tables can be configured with different states: `Queryable` (can be asked about directly), `Joinable` (only used for joins), or `Off` (completely hidden from the AI).

## Requirements
You have an existing Inconvo project at `/home/user/inconvo-project` with an `inconvo.yaml` file. Update the table states according to these rules:
- The `orders` table should remain `Queryable`.
- The `customers` table should be changed to `Joinable`.
- The `internal_logs` table should be changed to `Off`.

## Implementation Guide
1. Open `/home/user/inconvo-project/inconvo.yaml`.
2. Locate the `tables` section.
3. Modify the `state` property for `customers` to `Joinable`.
4. Modify the `state` property for `internal_logs` to `Off`.

## Constraints
- Project path: /home/user/inconvo-project