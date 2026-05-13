import os
import subprocess
import json
import pytest
import time

PROJECT_DIR = "/home/user/inconvo-project"

def test_inconvo_yaml_configuration():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()
    
    assert "state: Joinable" in content, "Expected customer_addresses table to have 'state: Joinable'"
    assert "left: customers.id" in content or "right: customers.id" in content, "Expected relationship using customers.id"
    assert "customer_addresses.customer_id" in content, "Expected relationship using customer_addresses.customer_id"

def test_conversation_api_behavior():
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    api_key = os.environ.get("INCONVO_API_KEY")
    
    assert agent_id, "INCONVO_AGENT_ID is not set"
    assert api_key, "INCONVO_API_KEY is not set"
    
    verify_script = """
import "dotenv/config";
import { randomUUID } from "node:crypto";
import Inconvo from "@inconvoai/node";

const inconvo = new Inconvo({ apiKey: process.env.INCONVO_API_KEY });

async function main() {
    try {
        const agentConvo = await inconvo.agents.conversations.create(
            process.env.INCONVO_AGENT_ID,
            {
                userIdentifier: randomUUID().toString(),
                userContext: {}
            }
        );

        // Test 1: Valid join query
        const joinResponse = await inconvo.agents.conversations.response.create(
            agentConvo.id,
            {
                agentId: process.env.INCONVO_AGENT_ID,
                message: "What cities do our customers live in?",
                stream: false
            }
        );

        // Test 2: Invalid direct query to joinable-only table
        const directResponse = await inconvo.agents.conversations.response.create(
            agentConvo.id,
            {
                agentId: process.env.INCONVO_AGENT_ID,
                message: "Show me all customer addresses",
                stream: false
            }
        );

        console.log(JSON.stringify({
            joinResponse: joinResponse,
            directResponse: directResponse
        }));
    } catch (e) {
        console.error(e.message);
        process.exit(1);
    }
}

main();
"""
    script_path = os.path.join(PROJECT_DIR, "verify.mjs")
    with open(script_path, "w") as f:
        f.write(verify_script)
    
    # Wait a moment to ensure model push propagated if it was just done
    time.sleep(2)
    
    result = subprocess.run(
        ["node", "verify.mjs"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Verification script failed: {result.stderr}\n{result.stdout}"
    
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse output as JSON: {result.stdout}")
        
    join_resp = output.get("joinResponse", {})
    direct_resp = output.get("directResponse", {})
    
    # The valid query should succeed and likely return a table or text with data
    join_text = json.dumps(join_resp).lower()
    assert "error" not in join_text or "message" in join_text, "Join query failed unexpectedly"
    
    # The direct query should fail to generate a SQL query for the unqueryable table
    # This might manifest as an error in generation, a fallback message, or refusal
    direct_text = json.dumps(direct_resp).lower()
    assert "error" in direct_text or "i cannot" in direct_text or "not available" in direct_text or "joinable" in direct_text or "cannot query" in direct_text or direct_resp.get('type') != 'table', \
        "Direct query to joinable-only table should have been rejected or failed to return a table"
