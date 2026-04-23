# Handling Unsupported Queries by Hiding Data

## Background
You have an Inconvo project initialized at `/home/user/myproject`. The semantic model `inconvo.yaml` exposes several tables, including a `users` table which currently exposes sensitive fields like `password_hash` as `On`, and an `internal_logs` table that is `Queryable`.
To ensure the Data Agent safely handles unsupported or sensitive queries by not exposing the data, we need to hide these fields and tables.

## Requirements
- Update the `users` table to make the `password_hash` field `Off` instead of `On`.
- Update the `internal_logs` table `state` from `Queryable` to `Off` so it cannot be queried at all.

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Locate the `users` table under `tables` and change the `state` of `password_hash` under `fields` to `Off`.
3. Locate the `internal_logs` table under `tables` and change its `state` to `Off`.
4. Save the file.

## Constraints
- Project path: /home/user/myproject