### 1. Library Overview
* **Description**: Inconvo is an open-source platform for building reliable, customer-facing "chat-with-data" agents. Unlike traditional AI-to-SQL approaches, Inconvo uses a **Semantic Layer** to map natural language questions into structured query plans that are validated against a predefined schema before being executed as SQL.
* **Ecosystem Role**: It acts as a middleware between LLMs and production databases, providing a safe, multi-tenant, and deterministic way to expose analytics to end users. It integrates seamlessly with the Vercel AI SDK and Node.js backends.
* **Project Setup**:
    1.  Install the CLI: `npm install -g inconvo` or use `npx inconvo@latest dev`.
    2.  Initialize a project: `inconvo init` (creates a default configuration and semantic model).
    3.  Configure the database: Set the `DATABASE_URL` environment variable (e.g., in a `.env` file).
    4.  Run the development server: `inconvo dev` (starts a local server that serves the agent and provides a preview interface).
### 2. Core Primitives & APIs
*   **Semantic Model (`inconvo.yaml`)**: The core configuration file where you define the "contract" between the AI and your data.
    *   **Tables**: Define which tables are `Queryable` (can be asked about), `Joinable` (only for joins), or `Off`.
    *   **Fields**: Define dimensions and measures, including visibility (`On`/`Off`) and synonyms.
    *   **Relationships**: Define join paths between tables (e.g., `orders.customer_id` -> `customers.id`).
*   **Conversations API**: Used to interact with the agent programmatically.
    *   `client.conversations.create({ context: { user_id: 123 } })`: Starts a new conversation with a specific tenant context.
    *   `client.conversations.messages.create(id, { message: "What are my top products?" })`: Sends a natural language query and receives a structured response (text, table, or chart).
*   **SDKs**:
    *   **Node.js**: `@inconvoai/node` for server-side integration.
    *   **Vercel AI SDK**: `@inconvoai/vercel-ai-sdk` for building streaming chat interfaces in React/Next.js.
**Code Example (Semantic Model Snippet):**
```yaml
tables:
  orders:
    state: Queryable
    fields:
      id: { state: On }
      total_amount: { state: On, type: measure }
      created_at: { state: On, type: dimension }
  customers:
    state: Joinable
    fields:
      name: { state: On }
relations:
  - name: order_to_customer
    left: orders.customer_id
    right: customers.id
```
### 3. Real-World Use Cases & Templates
*   **In-App Analytics**: Adding a "Ask anything about your data" button to a SaaS dashboard.
*   **Multi-tenant Reporting**: Scoping data so users can only query their own records using context filters.
*   **Customer Support Bots**: Giving support agents the ability to look up order statuses and history via natural language.
*   **Vercel AI SDK Integration**: Using Inconvo as a tool within a larger AI agent workflow to provide factual data visualizations.
### 4. Developer Friction Points
*   **Semantic Model Complexity**: Manually mapping large schemas with complex relationships and ambiguous column names can be time-consuming.
*   **Join Path Ambiguity**: If multiple join paths exist between tables, the agent may pick the wrong one unless explicitly constrained in the YAML.
*   **Context Mapping**: Correctly mapping application-level user IDs to database-level tenant IDs via the `context` object is a common source of authorization bugs.
### 5. Evaluation Ideas
*   **Project Initialization**: Initialize an Inconvo project and connect it to a PostgreSQL database using a provided `DATABASE_URL`.
*   **Schema Mapping**: Create a semantic model for an e-commerce database (Orders, Products, Users) where only specific fields are queryable.
*   **Relationship Definition**: Configure a many-to-one relationship between `LineItems` and `Products` to allow querying "What is the most popular product name?".
*   **Multi-tenant Authorization**: Implement a context filter on the `Orders` table that restricts queries to a specific `store_id` passed in the conversation context.
*   **Metric Definition**: Define a calculated measure for "Gross Margin" (Revenue - Cost) within the semantic layer.
*   **API Integration**: Build a simple Express.js endpoint that uses the `@inconvoai/node` SDK to forward user questions to the Inconvo dev server.
*   **Streaming UI**: Implement a React component using the Vercel AI SDK that renders an Inconvo `table` response as a formatted data grid.
### 6. Sources
1.  [Inconvo Official Website](https://inconvo.com/): Primary product information and high-level features.
2.  [Inconvo Documentation](https://inconvo.com/docs/getting-started/quickstart/): Quickstart guides and API references.
3.  [Inconvo Blog - Open Sourcing](https://inconvo.com/blog/open-sourcing-inconvo/): Details on the local dev environment and semantic model philosophy.
4.  [Inconvo Blog - No SQL Generation](https://inconvo.com/blog/how-we-built-a-chat-with-data-agent-that-doesnt-ai-generate-sql/): Technical deep-dive into the structured intent and validation layer.
5.  [NPM: @inconvoai/node](https://www.npmjs.com/package/@inconvoai/node): SDK usage and installation details.
6.  [NPM: inconvo (CLI)](https://www.npmjs.com/package/inconvo): CLI versioning and local development commands.
7.  [Y Combinator: Inconvo](https://www.ycombinator.com/companies/inconvo): Summary of the platform's core value proposition and architecture.
