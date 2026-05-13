import os
import subprocess
import pytest
import json

PROJECT_DIR = "/home/user/inconvo-project"

def test_inconvo_yaml_configured():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Semantic model {config_path} does not exist."
    
    with open(config_path, "r") as f:
        content = f.read()
    
    assert "sales:" in content, "The 'sales' table is not defined in inconvo.yaml."
    assert "Queryable" in content, "The 'sales' table must be marked as 'Queryable'."
    assert "created_at:" in content, "The 'created_at' field is not defined."
    assert "dimension" in content, "The 'created_at' field must be a 'dimension'."
    assert "amount:" in content, "The 'amount' field is not defined."
    assert "measure" in content, "The 'amount' field must be a 'measure'."

def test_inconvo_agent_can_answer_query():
    # Install the SDK for the test script
    subprocess.run(["npm", "install", "@inconvoai/node"], cwd=PROJECT_DIR, capture_output=True)
    
    # Write a small Node.js script to query the agent
    script_path = os.path.join(PROJECT_DIR, "test_query.mjs")
    script_content = """
import Inconvo from "@inconvoai/node";

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
  const agentConvo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {
      userIdentifier: "test-user-" + Date.now(),
      userContext: {},
    }
  );

  const agentResponse = await inconvo.agents.conversations.response.create(
    agentConvo.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "sales over time by month",
      stream: false,
    }
  );
  
  console.log(JSON.stringify(agentResponse));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
    """
    
    with open(script_path, "w") as f:
        f.write(script_content)
        
    result = subprocess.run(
        ["node", "test_query.mjs"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Query to Inconvo Agent failed: {result.stderr}\\n{result.stdout}"
    
    try:
        response_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse agent response as JSON: {result.stdout}")
    
    # We expect a successful response, perhaps containing some data or a chart about sales
    assert "error" not in response_data, f"Agent returned an error: {response_data}"
