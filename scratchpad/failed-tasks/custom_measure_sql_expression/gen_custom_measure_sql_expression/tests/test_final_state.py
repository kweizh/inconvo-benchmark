import os
import subprocess
import json
import yaml
import pytest
import time

PROJECT_DIR = "/home/user/inconvo-project"

def test_model_pull_and_yaml_verification():
    """Priority 1: Use CLI to pull the model and verify the YAML content."""
    # Pull the model
    result = subprocess.run(
        ["npx", "inconvo@latest", "model", "pull"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'inconvo model pull' failed: {result.stderr}"
    
    # Find the YAML file
    inconvo_dir = os.path.join(PROJECT_DIR, ".inconvo")
    assert os.path.isdir(inconvo_dir), f".inconvo directory not found in {PROJECT_DIR}"
    
    yaml_files = [f for f in os.listdir(inconvo_dir) if f.endswith(".yaml") or f.endswith(".yml")]
    assert len(yaml_files) > 0, "No YAML files found in .inconvo directory."
    
    # Check the YAML content
    orders_table_found = False
    completed_amount_found = False
    correct_sql = False
    is_measure = False
    
    for file_name in yaml_files:
        file_path = os.path.join(inconvo_dir, file_name)
        with open(file_path, "r") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError:
                continue
            
            tables = data.get("tables", {})
            if "orders" in tables:
                orders_table_found = True
                fields = tables["orders"].get("fields", {})
                if "completed_amount" in fields:
                    completed_amount_found = True
                    field_def = fields["completed_amount"]
                    if field_def.get("type") == "measure":
                        is_measure = True
                    sql_expr = field_def.get("sql", "")
                    if "SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END)" in sql_expr or "SUM(CASE WHEN status='completed' THEN amount ELSE 0 END)" in sql_expr:
                        correct_sql = True

    assert orders_table_found, "The 'orders' table was not found in the semantic model."
    assert completed_amount_found, "The 'completed_amount' field was not found on the 'orders' table."
    assert is_measure, "The 'completed_amount' field must have 'type: measure'."
    assert correct_sql, "The 'completed_amount' field does not have the correct SQL expression."

def test_agent_query_via_sdk():
    """Priority 1: Use the Inconvo SDK to verify the agent can answer queries about the new measure."""
    api_key = os.environ.get("INCONVO_API_KEY")
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    
    if not api_key or not agent_id:
        pytest.skip("INCONVO_API_KEY or INCONVO_AGENT_ID not set")
        
    # We write a small Node.js script to use the SDK since we are in a Python test
    script_path = os.path.join(PROJECT_DIR, "test_query.js")
    with open(script_path, "w") as f:
        f.write(f"""
const Inconvo = require('@inconvoai/node').default;
const crypto = require('crypto');

async function main() {{
  const inconvo = new Inconvo({{ apiKey: process.env.INCONVO_API_KEY }});
  
  const agentConvo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {{
      userIdentifier: crypto.randomUUID(),
      userContext: {{}}
    }}
  );
  
  const agentResponse = await inconvo.agents.conversations.response.create(
    agentConvo.id,
    {{
      agentId: process.env.INCONVO_AGENT_ID,
      message: "What is the completed amount?",
      stream: false,
    }}
  );
  
  console.log(JSON.stringify(agentResponse));
}}

main().catch(err => {{
  console.error(err);
  process.exit(1);
}});
""")
    
    # Ensure @inconvoai/node is installed
    subprocess.run(["npm", "install", "@inconvoai/node"], cwd=PROJECT_DIR, capture_output=True)
    
    result = subprocess.run(["node", "test_query.js"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"SDK query failed: {result.stderr}"
    
    try:
        response = json.loads(result.stdout)
        # Verify the response is successful and contains some data
        assert response, "Empty response from agent."
        # We don't assert the exact number because the DB might have different data if other tests ran,
        # but we assert the query succeeded without errors.
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse agent response as JSON: {result.stdout}")
