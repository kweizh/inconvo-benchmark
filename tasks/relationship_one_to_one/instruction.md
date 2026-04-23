# Inconvo One-to-One Relationship

## Background
You have an Inconvo project at `/home/user/myproject`. The project contains a semantic model file `inconvo.yaml` with two tables: `users` and `profiles`.

## Requirements
- Define a relationship between the `users` and `profiles` tables in the `inconvo.yaml` file.
- The relationship should be named `user_to_profile`.
- The `left` side of the relationship should be `users.profile_id`.
- The `right` side of the relationship should be `profiles.id`.

## Constraints
- Project path: `/home/user/myproject`
- File to edit: `/home/user/myproject/inconvo.yaml`

## Implementation Guide
1. Open `/home/user/myproject/inconvo.yaml`.
2. Add a `relations` list at the root level if it doesn't exist.
3. Add the `user_to_profile` relationship with the specified `left` and `right` fields.

## Integrations
- None