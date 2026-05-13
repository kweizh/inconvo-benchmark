import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"

def test_inconvo_yaml_contains_context_filters():
    """Verify that inconvo.yaml contains context filters for users and orders."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"
    
    with open(yaml_path, 'r') as f:
        content = f.read()
    
    # Check that users and orders tables exist
    assert "users:" in content, "The 'users' table is missing from inconvo.yaml"
    assert "orders:" in content, "The 'orders' table is missing from inconvo.yaml"
    
    # Check that context filters are applied
    # The exact syntax might vary slightly (e.g., context_filter, or WHERE clause)
    # but the task requires scoping by tenantId.
    assert "userContext.tenantId" in content, "The context filter using 'userContext.tenantId' is missing from inconvo.yaml"

def test_api_returns_filtered_data():
    """Verify that querying the agent respects the context filter using the Node.js SDK."""
    api_key = os.environ.get("INCONVO_API_KEY")
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    
    assert api_key, "INCONVO_API_KEY environment variable is not set."
    assert agent_id, "INCONVO_AGENT_ID environment variable is not set."
    
    # We will write a temporary JS script to query the Inconvo API
    js_script = """
import "dotenv/config";
import Inconvo from "@inconvoai/node";

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
    const agentConvo = await inconvo.agents.conversations.create(
        process.env.INCONVO_AGENT_ID,
        {
            userIdentifier: "test_user_1",
            userContext: {
                tenantId: 1
            }
        }
    );

    const response = await inconvo.agents.conversations.response.create(
        agentConvo.id,
        {
            agentId: process.env.INCONVO_AGENT_ID,
            message: "Count the number of users and orders.",
            stream: false
        }
    );

    console.log(JSON.stringify(response));
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
"""
    script_path = os.path.join(PROJECT_DIR, "test_api.mjs")
    with open(script_path, "w") as f:
        f.write(js_script)
    
    # Initialize a dummy package.json and install SDK if not present in PROJECT_DIR
    # Actually, we can just run it in a temp dir or PROJECT_DIR
    # Let's ensure the SDK is installed
    subprocess.run(["npm", "install", "@inconvoai/node", "dotenv"], cwd=PROJECT_DIR, capture_output=True)
    
    result = subprocess.run(["node", "test_api.mjs"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"API test script failed: {result.stderr}"
    
    output = result.stdout.lower()
    
    # We expect 2 users and 3 orders for tenant_id = 1
    assert "2" in output or "two" in output, f"Expected 2 users in the response, got: {output}"
    assert "3" in output or "three" in output, f"Expected 3 orders in the response, got: {output}"
    
    # Make sure it doesn't return the data for tenant_id = 2
    assert "5" not in output and "five" not in output, f"Response should not contain data from tenant 2 (5 users), got: {output}"
    assert "7" not in output and "seven" not in output, f"Response should not contain data from tenant 2 (7 orders), got: {output}"
