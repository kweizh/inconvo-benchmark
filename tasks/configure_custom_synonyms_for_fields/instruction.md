# Configure Custom Synonyms for Fields

## Background
Inconvo allows configuring synonyms for fields in the semantic model to improve natural language understanding. A database column might have a terse name like `dob`, but users might ask for "date of birth" or "birthday".

## Requirements
- Update the `inconvo.yaml` file to include synonyms for the `dob` field in the `customers` table.
- The synonyms should be "date of birth" and "birthday".
- Use the provided `DATABASE_URL` to verify that the project configuration is correct.

## Implementation
1. Navigate to the project directory `/home/user/myproject`.
2. Edit `inconvo.yaml` and add a `synonyms` array to the `dob` field under the `customers` table.

## Constraints
- Project path: `/home/user/myproject`