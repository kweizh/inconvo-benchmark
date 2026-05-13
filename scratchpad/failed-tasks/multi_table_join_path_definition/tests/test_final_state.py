import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"

def test_inconvo_yaml_tables():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path) as f:
        content = f.read()
    
    assert "orders:" in content, "Expected 'orders' table to be defined in inconvo.yaml."
    assert "users:" in content, "Expected 'users' table to be defined in inconvo.yaml."
    assert "organizations:" in content, "Expected 'organizations' table to be defined in inconvo.yaml."
    
    # Check states
    assert "Queryable" in content or "Joinable" in content, "Expected table states (Queryable/Joinable) to be defined."

def test_inconvo_yaml_relations():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path) as f:
        content = f.read()
    
    assert "relations:" in content, "Expected 'relations' section to be defined in inconvo.yaml."
    assert "orders.user_id" in content or "users.id" in content, "Expected relation between orders and users."
    assert "users.organization_id" in content or "organizations.id" in content, "Expected relation between users and organizations."

def test_inconvo_agent_query_success():
    api_key = os.environ.get("INCONVO_API_KEY")
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    
    assert api_key is not None, "INCONVO_API_KEY environment variable is not set."
    assert agent_id is not None, "INCONVO_AGENT_ID environment variable is not set."
    
    # Create a small Node.js script to query the agent
    script_path = os.path.join(PROJECT_DIR, "test_query.js")
    with open(script_path, "w") as f:
        f.write(f\"\"\"
const Inconvo = require("@inconvoai/node").default || require("@inconvoai/node");
const crypto = require("node:crypto");

const inconvo = new Inconvo({{
  apiKey: process.env.INCONVO_API_KEY,
}});

async function main() {{
  try {{
    const agentConvo = await inconvo.agents.conversations.create(
      process.env.INCONVO_AGENT_ID,
      {{
        userIdentifier: crypto.randomUUID().toString(),
      }}
    );

    const agentResponse = await inconvo.agents.conversations.response.create(
      agentConvo.id,
      {{
        agentId: process.env.INCONVO_AGENT_ID,
        message: "What are the total orders for Acme Corp?",
        stream: false,
      }}
    );
    
    console.log(JSON.stringify(agentResponse));
  }} catch (e) {{
    console.error(e);
    process.exit(1);
  }}
}}

main();
\"\"\")

    # Run the script
    result = subprocess.run(
        ["node", "test_query.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Query to Inconvo agent failed: {result.stderr}\\nStdout: {result.stdout}"
    
    output = result.stdout
    assert output.strip() != "", "No output received from the agent."
    
    # Optional: parse JSON and verify it contains a valid response
    try:
        response_json = json.loads(output)
        assert response_json is not None, "Response JSON is null."
        # We don't strictly assert the exact value because it depends on the agent's LLM response,
        # but a successful HTTP 200 response with data indicates the join path works.
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse agent response as JSON: {output}")
