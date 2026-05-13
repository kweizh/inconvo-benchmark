import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")


def _field_block(content: str, field_name: str) -> str:
    parts = content.split(f"{field_name}:")
    assert len(parts) >= 2, f"Expected '{field_name}:' declaration in inconvo.yaml."
    # Take everything up to and including the next 2 lines so we capture inline { ... } blocks.
    return parts[1].split("\n", 2)[0]


def test_email_state_off():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"
    with open(YAML_FILE, "r") as f:
        content = f.read()
    block = _field_block(content, "email")
    assert "Off" in block, (
        f"Expected customers.email to have 'state: Off' in inconvo.yaml. Got block: {block}"
    )
    assert "On" not in block.replace("Off", ""), (
        f"customers.email block still contains 'On' after removing 'Off' marker: {block}"
    )


def test_phone_state_off():
    with open(YAML_FILE, "r") as f:
        content = f.read()
    block = _field_block(content, "phone")
    assert "Off" in block, (
        f"Expected customers.phone to have 'state: Off' in inconvo.yaml. Got block: {block}"
    )
    assert "On" not in block.replace("Off", ""), (
        f"customers.phone block still contains 'On' after removing 'Off' marker: {block}"
    )


def test_non_pii_fields_still_on():
    with open(YAML_FILE, "r") as f:
        content = f.read()

    # customers.name must still be On
    name_block = _field_block(content, "name")
    assert "On" in name_block and "Off" not in name_block, (
        f"Expected customers.name to remain 'state: On'. Got block: {name_block}"
    )

    # orders.total_amount must still be On
    total_block = _field_block(content, "total_amount")
    assert "On" in total_block and "Off" not in total_block, (
        f"Expected orders.total_amount to remain 'state: On'. Got block: {total_block}"
    )


def test_index_js_exists_and_references_sdk():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"
    with open(INDEX_JS, "r") as f:
        content = f.read()
    assert "@inconvoai/node" in content, "Expected index.js to import/require @inconvoai/node."
    assert "INCONVO_AGENT_ID" in content, "Expected index.js to reference INCONVO_AGENT_ID env var."
    assert "List customer names and their total orders" in content, (
        "Expected index.js to send the natural language query "
        "'List customer names and their total orders'."
    )


def test_run_index_js_produces_response():
    env = os.environ.copy()
    assert env.get("INCONVO_API_KEY"), "INCONVO_API_KEY must be set in the verifier environment."
    assert env.get("INCONVO_AGENT_ID"), "INCONVO_AGENT_ID must be set in the verifier environment."

    # Remove any stale response.json from previous runs.
    if os.path.exists(RESPONSE_FILE):
        os.remove(RESPONSE_FILE)

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env,
        timeout=180,
    )
    assert result.returncode == 0, (
        f"'node index.js' failed with stderr:\n{result.stderr}\nstdout:\n{result.stdout}"
    )


def test_response_json_is_valid_and_non_error():
    assert os.path.isfile(RESPONSE_FILE), f"response.json not found at {RESPONSE_FILE}"
    with open(RESPONSE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("response.json is not valid JSON.")

    if isinstance(data, dict):
        assert data.get("error") is not True, (
            f"response.json indicates an error payload: {data}"
        )

    content_str = json.dumps(data).lower()
    assert any(
        keyword in content_str
        for keyword in ("table", "rows", "data", "message", "type")
    ), f"response.json does not appear to contain a real Inconvo response. Content: {data}"
