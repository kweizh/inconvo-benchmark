import os
import re
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")


def _read(path):
    with open(path, "r") as f:
        return f.read()


def test_inconvo_yaml_contains_gross_margin_measure():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"
    content = _read(YAML_FILE)

    assert "gross_margin" in content, \
        "Expected 'gross_margin' field to be added to inconvo.yaml."

    # Inspect the block immediately following the gross_margin key.
    block = content.split("gross_margin", 1)[1]
    # Limit to a reasonable window so we don't pick up other unrelated fields.
    window = block[:400].lower()

    assert "measure" in window, \
        f"Expected 'gross_margin' to be declared with type 'measure'. Block was: {window!r}"
    assert "total_amount" in window, \
        f"Expected 'gross_margin' expression to reference 'total_amount'. Block was: {window!r}"
    assert "cost" in window, \
        f"Expected 'gross_margin' expression to reference 'cost'. Block was: {window!r}"
    assert "-" in window, \
        f"Expected 'gross_margin' expression to use the '-' operator. Block was: {window!r}"


def test_index_js_exists_and_uses_inconvo_sdk():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"
    content = _read(INDEX_JS)

    assert "@inconvoai/node" in content, \
        "Expected '@inconvoai/node' to be imported/required in index.js."
    # The script should ask for average gross margin per month.
    assert re.search(r"gross\s*margin", content, re.IGNORECASE), \
        "Expected index.js to send a message mentioning gross margin."
    assert "response.json" in content, \
        "Expected index.js to write the response to response.json."


def test_run_index_js_produces_response():
    env = os.environ.copy()
    for var in ("INCONVO_API_KEY", "INCONVO_AGENT_ID", "INCONVO_DB_URL"):
        assert env.get(var), \
            f"Required environment variable {var} is not set for the verifier."

    # Remove any stale response from previous runs so we know the script wrote it.
    if os.path.isfile(RESPONSE_FILE):
        os.remove(RESPONSE_FILE)

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )
    assert result.returncode == 0, \
        f"'node index.js' failed with code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"


def test_response_json_is_valid_and_non_empty():
    assert os.path.isfile(RESPONSE_FILE), \
        f"response.json was not produced at {RESPONSE_FILE}"

    raw = _read(RESPONSE_FILE).strip()
    assert raw, "response.json is empty."

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        pytest.fail(f"response.json is not valid JSON: {e}\nContent: {raw!r}")

    # The response must not be an obvious error.
    if isinstance(data, dict):
        assert data.get("error") not in (True, "true"), \
            f"response.json indicates an error: {data}"
        if "status" in data and isinstance(data["status"], (int, str)):
            status_val = str(data["status"])
            assert not status_val.startswith("4") and not status_val.startswith("5"), \
                f"response.json indicates an HTTP error status: {data}"

    # The response should be non-trivial: contain typical Inconvo response keys
    # or at least be a sufficiently rich structure (not just {}).
    content_str = json.dumps(data).lower()
    assert len(content_str) > 10, \
        f"response.json content is too small to be a real Inconvo response: {data}"
    assert any(
        keyword in content_str
        for keyword in ("table", "rows", "data", "text", "chart", "message", "response", "answer", "value")
    ), f"response.json does not look like a real Inconvo Data Agent response: {data}"
