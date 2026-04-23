# Healthcare Schema Mapping

## Background
You are building an Inconvo Data Agent for a healthcare application. Inconvo uses a Semantic Model (`inconvo.yaml`) to map natural language to a predefined schema.

## Requirements
Create a semantic model for a healthcare database with the following structure:

1.  **patients** table:
    -   State: `Queryable`
    -   Fields:
        -   `id`: `On`, type `dimension`
        -   `birth_date`: `On`, type `dimension`
2.  **encounters** table:
    -   State: `Queryable`
    -   Fields:
        -   `id`: `On`, type `dimension`
        -   `total_cost`: `On`, type `measure`
        -   `patient_id`: `On`, type `dimension`
        -   `practitioner_id`: `On`, type `dimension`
3.  **practitioners** table:
    -   State: `Joinable`
    -   Fields:
        -   `id`: `On`, type `dimension`
        -   `name`: `On`, type `dimension`
4.  **relations**:
    -   `patient_encounters`: Join `encounters.patient_id` to `patients.id`.
    -   `practitioner_encounters`: Join `encounters.practitioner_id` to `practitioners.id`.

## Implementation Guide
1.  Create or update the `inconvo.yaml` file in the project directory.
2.  Define the `tables` block with `patients`, `encounters`, and `practitioners`, including their respective states and fields.
3.  Define the `relations` block containing the two specified joins.

## Constraints
- Project path: `/home/user/healthcare-agent`
- The file must be named `inconvo.yaml` and placed in the project path.
