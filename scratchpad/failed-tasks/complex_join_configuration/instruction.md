While Inconvo can automatically detect standard foreign keys, complex or non-obvious relationships must be explicitly mapped so the AI knows how to join tables when answering cross-domain questions.

You need to define a `relation` in the semantic model explicitly linking the `employees` table and the `departments` table using the `department_id` key.

**Constraints:**
- The join path must be explicitly written in the `.inconvo/` configuration files.
- You must define the relation type (e.g., one-to-many or many-to-one).
- Do not add explicit foreign key constraints to the actual database schema to solve this task.