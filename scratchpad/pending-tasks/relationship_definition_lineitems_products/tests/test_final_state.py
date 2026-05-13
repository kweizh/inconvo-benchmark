import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_agent_query():
    """Priority 1: Query the Inconvo cloud API to verify the agent can answer the question."""
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    api_key = os.environ.get("INCONVO_API_KEY")
    
    assert agent_id, "INCONVO_AGENT_ID is not set"
    assert api_key, "INCONVO_API_KEY is not set"
    
    ts_script = """
import Inconvo from "@inconvoai/node";
import * as crypto from "crypto";

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
    const agentConvo = await inconvo.agents.conversations.create(
        process.env.INCONVO_AGENT_ID,
        {
            userIdentifier: crypto.randomUUID().toString(),
        }
    );
    
    const agentResponse = await inconvo.agents.conversations.response.create(
        agentConvo.id,
        {
            agentId: process.env.INCONVO_AGENT_ID,
            message: "What is the most popular product name?",
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
    
    script_path = os.path.join(PROJECT_DIR, "test_script.ts")
    with open(script_path, "w") as f:
        f.write(ts_script)
        
    env = os.environ.copy()
    result = subprocess.run(["tsx", script_path], capture_output=True, text=True, env=env, cwd=PROJECT_DIR)
    
    assert result.returncode == 0, f"TypeScript script failed: {result.stderr}"
    
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response: {result.stdout}")
        
    # The most popular product name based on the initial DB setup:
    # Laptop: 5 + 2 = 7
    # Mouse: 20 + 5 = 25
    # Keyboard: 10
    # So "Mouse" is the most popular.
    
    response_text = json.dumps(response).lower()
    assert "mouse" in response_text, f"Expected 'Mouse' in the response, got: {result.stdout}"

def test_inconvo_yaml_exists_and_configured():
    """Priority 3 fallback: Verify the inconvo.yaml file contains the necessary configurations."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"
    
    with open(yaml_path, "r") as f:
        content = f.read()
        
    assert "line_items" in content, "Expected 'line_items' table in inconvo.yaml"
    assert "products" in content, "Expected 'products' table in inconvo.yaml"
    assert "relations:" in content or "relationships:" in content, "Expected relations to be defined in inconvo.yaml"
