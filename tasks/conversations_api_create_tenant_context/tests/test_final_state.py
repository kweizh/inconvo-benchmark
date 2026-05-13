import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
OUTPUT_JSON = os.path.join(PROJECT_DIR, "output.json")

def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"

def test_index_js_contents():
    with open(INDEX_JS, "r") as f:
        content = f.read()
    
    assert "conversations.create" in content, "Expected client.conversations.create to be called in index.js"
    assert "tenant_456" in content, "Expected tenant_456 context to be used in index.js"
    assert "@inconvoai/node" in content, "Expected @inconvoai/node to be imported in index.js"

def test_run_index_js():
    # Provide dummy env vars so the script can run
    env = os.environ.copy()
    if "INCONVO_API_KEY" not in env:
        env["INCONVO_API_KEY"] = "dummy_key"
    if "INCONVO_AGENT_ID" not in env:
        env["INCONVO_AGENT_ID"] = "dummy_agent"

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"

def test_output_json_exists_and_valid():
    assert os.path.isfile(OUTPUT_JSON), f"output.json not found at {OUTPUT_JSON}"

    with open(OUTPUT_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("output.json is not valid JSON")
    
    # Since we used dummy credentials, it might be an error or a conversation object
    content_str = json.dumps(data).lower()
    assert "error" in content_str or "message" in content_str or "id" in content_str, \
        f"output.json doesn't seem to contain expected API response. Content: {data}"
