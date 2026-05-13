### 1. Library Overview
* **Description**: Inconvo is an open-source platform for building reliable, customer-facing "chat-with-data" agents. Unlike traditional AI-to-SQL approaches, Inconvo uses a **Semantic Layer** to map natural language questions into structured query plans that are validated against a predefined schema before being executed as SQL.
* **Ecosystem Role**: It acts as a middleware between LLMs and production databases, providing a safe, multi-tenant, and deterministic way to expose analytics to end users. It integrates seamlessly with the Vercel AI SDK and Node.js backends.
* **Project Setup**:
    1.  **Inconvo Cloud Setup**: Create an account on Inconvo Cloud (app.inconvo.ai), create a Data Agent, and obtain your Agent ID and API Key.
    2.  **Environment Variables**: You MUST set `INCONVO_API_KEY`, `INCONVO_AGENT_ID`, and the database URL (e.g., `DATABASE_URL` or `INCONVO_DB_URL`) in your `.env` file. These are explicitly required for later usage in generation tasks and connecting to the cloud agent.
    3.  **Database Connection**: Connect your PostgreSQL database in the Inconvo app (providing Host, Port, Username, Password, and Database Name).
    4.  **SDK & Semantic Layer**: Install the SDK (`npm i @inconvoai/node dotenv`). Use the Inconvo CLI/skills (`npx skills add inconvoai/inconvo` and `npx inconvo model pull`) to pull and update your semantic model locally.
    5.  **Run**: Write code using `@inconvoai/node` to call your Data Agent using the configured environment variables.
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

** Code Example (Inconvo):**

index.ts

```javascript
import "dotenv/config";
import { randomUUID } from "node:crypto";
import Inconvo from "@inconvoai/node";

const inconvo = new Inconvo({
  apiKey: process.env.INCONVO_API_KEY,
});

async function main() {
  const agentConvo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID!,
    {
      userIdentifier: randomUUID().toString(),
      userContext: {
        organisationId: 1,
      }, // NOTE: This is userContext for DemoAgent - change as needed
    },
  );

  const agentResponse = await inconvo.agents.conversations.response.create(
    agentConvo.id!,
    {
      agentId: process.env.INCONVO_AGENT_ID!,
      message: "Hello agent!",
      stream: false,
    },
  );
  console.log(agentResponse);
}

main().catch(console.error);
```

**Code Example (Vercel AI SDK):**

Should request the OPENAI_API_KEY in env.

app/api/chat/route.ts

```javascript
import { streamText, convertToModelMessages, stepCountIs } from "ai";
import { inconvoDataAgent } from "@inconvoai/vercel-ai-sdk";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: "openai/gpt-4", // or your preferred model
    system: `When you receive structured data (tables, charts) from tools,
      do NOT recreate or reformat them as markdown tables in your response.
      The tool output will be displayed directly as interactive UI.
      You may provide brief context, insights, or follow-up suggestions,
      but never duplicate the data itself.`,
    messages: await convertToModelMessages(messages),
    tools: {
      ...inconvoDataAgent({
        agentId: process.env.INCONVO_AGENT_ID!,
        userIdentifier: "user-123",
        userContext: {
          organisationId: 1,
        },
      }),
    },
    stopWhen: stepCountIs(5),
  });

  return result.toUIMessageStreamResponse();
}
```

app/page.tsx

```javascript
"use client";

import { useChat } from "@ai-sdk/react";
import { useState } from "react";
import { InconvoToolResult } from "./components/inconvo/InconvoToolResult";

function isInconvoOutput(output: unknown): boolean {
  return (
    typeof output === "object" &&
    output !== null &&
    "type" in output &&
    typeof (output as any).type === "string" &&
    ["text", "table", "chart"].includes((output as any).type)
  );
}

export default function Chat() {
  const [input, setInput] = useState("");
  const { messages, sendMessage } = useChat();

  return (
    <div className="flex flex-col w-full max-w-4xl py-24 mx-auto px-4">
      {messages.map((message) => (
        <div key={message.id} className="mb-4">
          <div className="font-semibold mb-1">
            {message.role === "user" ? "User" : "AI"}:
          </div>
          <div>
            {message.parts.map((part, i) => {
              if (part.type === "text") {
                return (
                  <div
                    key={`${message.id}-${i}`}
                    className="whitespace-pre-wrap"
                  >
                    {part.text}
                  </div>
                );
              }

              // Handle Inconvo tool calls
              if (part.type.startsWith("tool-") && "state" in part) {
                const isInconvoTool = part.type.includes("DataAgent");

                // Show loading state while tool is executing
                if (part.state === "input-available" && isInconvoTool) {
                  return (
                    <div
                      key={`${message.id}-${i}`}
                      className="flex items-center gap-2 p-4 text-sm text-zinc-500"
                    >
                      <div className="animate-spin h-4 w-4 border-2 border-zinc-300 border-t-zinc-600 rounded-full" />
                      <div>Querying your data...</div>
                    </div>
                  );
                }

                // Show result when available
                if (
                  part.state === "output-available" &&
                  "output" in part &&
                  isInconvoOutput(part.output)
                ) {
                  return (
                    <InconvoToolResult
                      key={`${message.id}-${i}`}
                      result={part.output}
                    />
                  );
                }
              }

              return null;
            })}
          </div>
        </div>
      ))}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage({ text: input });
          setInput("");
        }}
      >
        <input
          className="fixed bottom-0 w-full max-w-4xl p-2 mb-8 border border-zinc-300 rounded shadow-xl"
          value={input}
          placeholder="Ask about your data..."
          onChange={(e) => setInput(e.currentTarget.value)}
        />
      </form>
    </div>
  );
}
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

### 7. Benchmark References

When generating benchmark tasks,
you MUST follow the following rules:

1. MUST use INCONVO_API_KEY, INCONVO_AGENT_ID, and INCONVO_DB_URL env variables to perform real-world evaluations.
2. MUST NOT use any hardcoded values.
3. NEVER mock any dependencies, should always use real dependencies.
4. MUST setup database tables and rows in the initial test using INCONVO_DB_URL, also make sure the initial test could be run multiple times.


When writing `tests/test_final_state.py`, you should NEVER generate final tests that only validate the `inconvo.yaml` config. You SHOULD always run the script and validate the response and database status if necessary. Take the following script as a reference example:

```python
import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

def test_inconvo_yaml_exists_and_contains_tables():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

    with open(yaml_path, "r") as f:
        content = f.read()

    assert "orders" in content, "Expected 'orders' table definition in inconvo.yaml"
    assert "products" in content, "Expected 'products' table definition in inconvo.yaml"

def test_run_index_js():
    # Run the script that interacts with the SDK
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"

def test_response_json_exists_and_valid():
    assert os.path.isfile(RESPONSE_FILE), f"response.json not found at {RESPONSE_FILE}"

    with open(RESPONSE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("response.json is not valid JSON")

    if isinstance(data, dict):
        assert data.get("error") is not True, f"output.json indicates an error: {data}"

    # Check if it contains some table structure
    # The actual structure depends on the SDK, but we expect some kind of table/data response
    content_str = json.dumps(data).lower()
    assert "table" in content_str or "data" in content_str or "rows" in content_str, \
        f"response.json does not seem to contain table data. Content: {data}"
```

NEVER create a final test that only checks the content of configuration file, like:

```python
import os
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_gross_margin_field_exists():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"

    with open(YAML_FILE, "r") as f:
        content = f.read()

    assert "gross_margin:" in content, "Expected 'gross_margin' field to be added to inconvo.yaml"

def test_gross_margin_is_measure_and_has_formula():
    with open(YAML_FILE, "r") as f:
        content = f.read().lower()

    # Since we can't use pyyaml, we will do a broader check
    # We want to ensure that "measure" and "revenue" and "cost" and "-" appear after "gross_margin:"
    # This is a bit loose but works for verifying the LLM's output
    assert "gross_margin:" in content, "Could not find gross_margin line"

    parts = content.split("gross_margin:")
    after_gross_margin = parts[1]

    # We only look at the first few lines after gross_margin:
    lines_after = after_gross_margin.split('\n')[:5]
    block = " ".join(lines_after)

    assert "measure" in block, f"Expected 'gross_margin' to have type 'measure', found in block: {block}"
    assert "revenue" in block and "cost" in block and "-" in block, \
        f"Expected 'gross_margin' to compute 'revenue - cost', found in block: {block}"
```
