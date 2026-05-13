import os
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-agent"

def test_inconvo_yaml_exists_and_contains_tables():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

    with open(yaml_path, "r") as f:
        content = f.read()

    assert "orders" in content, "Expected 'orders' table definition in inconvo.yaml"
    assert "customers" in content, "Expected 'customers' table definition in inconvo.yaml"

def test_agent_js_imports():
    js_path = os.path.join(PROJECT_DIR, "agent.js")
    assert os.path.isfile(js_path), f"agent.js not found at {js_path}"
    
    with open(js_path, "r") as f:
        content = f.read()
        
    assert "@inconvoai/vercel-ai-sdk" in content, "agent.js must import @inconvoai/vercel-ai-sdk"
    assert "@ai-sdk/openai" in content, "agent.js must import @ai-sdk/openai"
    assert "generateText" in content, "agent.js must use generateText from ai sdk"

def test_response_json_exists_and_valid():
    response_path = os.path.join(PROJECT_DIR, "response.json")
    assert os.path.isfile(response_path), f"response.json not found at {response_path}"

    with open(response_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("response.json is not valid JSON")

    content_str = json.dumps(data).lower()
    assert "response" in content_str or "text" in content_str or "answer" in content_str, \
        f"response.json does not seem to contain the agent's textual response. Content: {data}"
