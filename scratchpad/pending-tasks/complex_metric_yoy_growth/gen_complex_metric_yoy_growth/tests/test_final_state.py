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
    
    # Check for computed column definition in YAML
    assert "yoy_growth" in content, "The 'yoy_growth' computed column is not defined in inconvo.yaml."
    assert "revenue_current" in content and "revenue_previous" in content, "The expression does not contain the required columns."
    assert "%" in content, "The unit '%' is not configured."

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
      message: "What is the yoy growth for 2026?",
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
        
    # Before testing the query, the semantic model must be pushed/synced. 
    # We will assume the user has done `inconvo model action run` or pushed it.
    # To be safe, we can run `inconvo model push` if it exists, or just rely on the user's setup.
    # Actually, the user's task might just be to modify inconvo.yaml, so let's push it to make sure.
    # Wait, the inconvo CLI doesn't have a `push` command. The CLI commands modify the cloud directly if using `--agent`.
    # Wait, if they modify inconvo.yaml, how does it sync?
    # `inconvo dev` syncs it, or `inconvo model pull` pulls it.
    # Let's just run the query and check.
    
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
    
    assert "error" not in response_data, f"Agent returned an error: {response_data}"
