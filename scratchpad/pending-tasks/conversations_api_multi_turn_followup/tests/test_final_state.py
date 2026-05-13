import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
CONVERSATION_ID_FILE = os.path.join(PROJECT_DIR, "conversation_id.txt")
FIRST_RESPONSE_FILE = os.path.join(PROJECT_DIR, "first_response.json")
SECOND_RESPONSE_FILE = os.path.join(PROJECT_DIR, "second_response.json")


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"


def test_run_index_js():
    """Run the multi-turn script against the real Inconvo Data Agent."""
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, \
        f"'node index.js' failed with output:\nSTDERR: {result.stderr}\nSTDOUT: {result.stdout}"


def test_conversation_id_file_contains_non_empty_id():
    assert os.path.isfile(CONVERSATION_ID_FILE), \
        f"conversation_id.txt not found at {CONVERSATION_ID_FILE}"

    with open(CONVERSATION_ID_FILE, "r") as f:
        conv_id = f.read().strip()

    assert conv_id, "conversation_id.txt is empty; expected a non-empty conversation id."
    assert len(conv_id) >= 4, \
        f"conversation_id.txt content seems too short to be a real id: '{conv_id}'"


def _load_response(path):
    assert os.path.isfile(path), f"Response file not found at {path}"
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not valid JSON")


def _assert_real_response(data, path):
    if isinstance(data, dict):
        assert data.get("error") is not True, \
            f"{path} indicates an error: {data}"

    content_str = json.dumps(data).lower()
    assert len(content_str) > 20, \
        f"{path} seems too short or empty. Content: {data}"
    assert any(token in content_str for token in ("data", "table", "text", "rows", "chart", "value")), \
        f"{path} does not look like a real Inconvo response. Content: {data}"


def test_first_response_is_valid_real_response():
    data = _load_response(FIRST_RESPONSE_FILE)
    _assert_real_response(data, FIRST_RESPONSE_FILE)


def test_second_response_is_valid_real_response():
    data = _load_response(SECOND_RESPONSE_FILE)
    _assert_real_response(data, SECOND_RESPONSE_FILE)


def test_index_js_sends_multi_turn_followup():
    """index.js must send two messages on the same conversation id (multi-turn)."""
    with open(INDEX_JS, "r") as f:
        content = f.read()

    assert "response.create" in content, \
        "Expected index.js to call inconvo.agents.conversations.response.create."
    assert content.count("response.create") >= 2, \
        "Expected index.js to call response.create at least twice for a multi-turn conversation."
    assert "top 5 customers" in content.lower(), \
        "Expected the first prompt about top 5 customers in index.js."
    assert "united states" in content.lower(), \
        "Expected the followup prompt referencing the United States in index.js."
