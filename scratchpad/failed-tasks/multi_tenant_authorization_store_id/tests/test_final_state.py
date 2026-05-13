import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_inconvo_yaml_contains_context_filter():
    """Priority 3: Check that inconvo.yaml has the context filter configured."""
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"
    
    with open(yaml_path, "r") as f:
        content = f.read()
    
    # We expect some reference to context.store_id
    assert "context.store_id" in content or "store_id" in content, \
        f"Expected context filter for store_id in inconvo.yaml, got: {content}"

def test_index_ts_queries_correctly():
    """Priority 1: Run the user's index.ts script and verify it returns correct count for store_id 1."""
    script_path = os.path.join(PROJECT_DIR, "index.ts")
    assert os.path.isfile(script_path), f"index.ts not found at {script_path}"
    
    env = os.environ.copy()
    
    result = subprocess.run(
        ["npx", "tsx", "index.ts"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 0, f"index.ts failed to run: {result.stderr}"
    output = result.stdout.lower()
    
    # store_id = 1 has 3 orders (from initial state)
    assert "3" in output, f"Expected the answer to be 3 orders for store_id=1, but got output: {result.stdout}"

def test_tenant_2_queries_correctly():
    """Priority 1: Create a test script for store_id 2 and verify it returns correct count."""
    script_path = os.path.join(PROJECT_DIR, "test_tenant_2.ts")
    
    # We will generate a script similar to index.ts but with store_id = 2
    # Since we can't reliably parse their index.ts and modify it, we will write our own
    # minimal test script using @inconvoai/node to test the deployed model.
    
    test_script = """
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
        store_id: 2,
      },
    },
  );

  const agentResponse = await inconvo.agents.conversations.response.create(
    agentConvo.id!,
    {
      agentId: process.env.INCONVO_AGENT_ID!,
      message: "How many orders do we have?",
      stream: false,
    },
  );
  
  console.log(JSON.stringify(agentResponse));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
"""
    with open(script_path, "w") as f:
        f.write(test_script)
        
    env = os.environ.copy()
    
    result = subprocess.run(
        ["npx", "tsx", "test_tenant_2.ts"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 0, f"test_tenant_2.ts failed to run: {result.stderr}"
    output = result.stdout
    
    # store_id = 2 has 5 orders (from initial state)
    assert "5" in output, f"Expected the answer to be 5 orders for store_id=2, but got output: {result.stdout}"
