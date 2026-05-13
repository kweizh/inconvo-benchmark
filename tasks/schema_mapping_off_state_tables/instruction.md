# Exclude Sensitive Tables

## Background
Inconvo uses a Semantic Model (`inconvo.yaml`) to define the contract between the AI and your data. You have an existing project with a semantic model where a sensitive table `passwords` is currently exposed.

## Requirements
- Update the semantic model to exclude the `passwords` table by setting its state to `Off`.

## Implementation Guide
1. Go to `/home/user/app`.
2. Open `inconvo.yaml`.
3. Change the `state` of the `passwords` table to `Off`.

## Constraints
- Project path: /home/user/app
- Do not modify the `users` table definition.

## Integrations
- None