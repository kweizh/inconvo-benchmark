import json
import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
USERS_JSON = os.path.join(PROJECT_DIR, "users.json")
RESPONSES_DIR = os.path.join(PROJECT_DIR, "responses")
ALICE_RESPONSE = os.path.join(RESPONSES_DIR, "alice-001.json")
BOB_RESPONSE = os.path.join(RESPONSES_DIR, "bob-002.json")
CONVERSATION_IDS = os.path.join(PROJECT_DIR, "conversation_ids.json")

EXPECTED_USER_IDS = ["alice-001", "bob-002"]


@pytest.fixture(scope="module")
def run_index_js():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}."
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, (
        f"'node index.js' failed (rc={result.returncode}).\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return result


def test_users_json_unchanged():
    assert os.path.isfile(USERS_JSON), f"users.json missing at {USERS_JSON}."
    with open(USERS_JSON, "r") as f:
        data = json.load(f)
    assert data == EXPECTED_USER_IDS, (
        f"users.json must remain {EXPECTED_USER_IDS}, got: {data}."
    )


def test_alice_response_file(run_index_js):
    assert os.path.isfile(ALICE_RESPONSE), f"Expected response file {ALICE_RESPONSE} to exist."
    with open(ALICE_RESPONSE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{ALICE_RESPONSE} is not valid JSON: {exc}")
    assert data, f"{ALICE_RESPONSE} is empty/falsy: {data!r}."
    content_str = json.dumps(data).lower()
    assert len(content_str) > 2, f"{ALICE_RESPONSE} appears to have no real response payload."


def test_bob_response_file(run_index_js):
    assert os.path.isfile(BOB_RESPONSE), f"Expected response file {BOB_RESPONSE} to exist."
    with open(BOB_RESPONSE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{BOB_RESPONSE} is not valid JSON: {exc}")
    assert data, f"{BOB_RESPONSE} is empty/falsy: {data!r}."
    content_str = json.dumps(data).lower()
    assert len(content_str) > 2, f"{BOB_RESPONSE} appears to have no real response payload."


def test_conversation_ids_file(run_index_js):
    assert os.path.isfile(CONVERSATION_IDS), (
        f"Expected mapping file {CONVERSATION_IDS} to exist."
    )
    with open(CONVERSATION_IDS, "r") as f:
        try:
            mapping = json.load(f)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{CONVERSATION_IDS} is not valid JSON: {exc}")

    assert isinstance(mapping, dict), (
        f"{CONVERSATION_IDS} must contain a JSON object, got: {type(mapping).__name__}."
    )

    for user_id in EXPECTED_USER_IDS:
        assert user_id in mapping, (
            f"Expected key '{user_id}' in conversation_ids.json, got keys: {list(mapping.keys())}."
        )
        value = mapping[user_id]
        assert isinstance(value, str) and value.strip(), (
            f"Conversation id for '{user_id}' must be a non-empty string, got: {value!r}."
        )

    ids = [mapping[u] for u in EXPECTED_USER_IDS]
    assert len(set(ids)) == len(ids), (
        f"Conversation ids for the different users must be distinct, got: {ids}."
    )
