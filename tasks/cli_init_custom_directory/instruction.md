# Initialize Inconvo Project Manually

## Background
You need to initialize a new Inconvo project in a specific directory. Although some documentation might mention an `inconvo init` command, the current `inconvo` CLI does not support it. Therefore, you must initialize the project manually.

## Requirements
- Create a directory at `/home/user/my-agent`.
- Create an `inconvo.yaml` file inside `/home/user/my-agent`.
- The `inconvo.yaml` file must contain a basic semantic model structure with an empty `tables` object and an empty `relations` array.

## Implementation Guide
1. Create the target directory `/home/user/my-agent`.
2. Create the file `/home/user/my-agent/inconvo.yaml`.
3. Add the following YAML content to the file:
```yaml
tables: {}
relations: []
```

## Constraints
- Project path: /home/user/my-agent

## Integrations
- None