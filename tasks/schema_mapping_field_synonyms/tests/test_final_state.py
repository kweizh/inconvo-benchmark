import json
import os
import re
import subprocess

import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INCONVO_YAML = os.path.join(PROJECT_DIR, "inconvo.yaml")
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")

TOTAL_AMOUNT_SYNONYMS = ["revenue", "sales", "income"]
CUSTOMER_NAME_SYNONYMS = ["customer", "buyer", "client"]


def _read(path):
    with open(path, "r") as f:
        return f.read()


def _block_between(content: str, header_re: str, end_re: str) -> str:
    """Return the substring between the first match of header_re and the first match of end_re after it."""
    m = re.search(header_re, content)
    assert m, f"Could not locate section matching: {header_re}"
    rest = content[m.end():]
    e = re.search(end_re, rest)
    return rest[: e.start()] if e else rest


def test_inconvo_yaml_exists():
    assert os.path.isfile(INCONVO_YAML), f"inconvo.yaml not found at {INCONVO_YAML}"


def test_total_amount_synonyms_present():
    content = _read(INCONVO_YAML)
    # Locate the block under orders -> fields -> total_amount and confirm all 3 synonyms appear.
    # We scope by extracting the chunk starting at total_amount until the next field key
    # ("created_at" sits after it in the starter file, but the agent may reorder, so fall back
    # to a generous window).
    block = _block_between(content, r"total_amount\s*:", r"\n[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*\n")
    # Provide a generous fallback if the regex above doesn't match a closing key
    search_text = block if block else content
    for word in TOTAL_AMOUNT_SYNONYMS:
        assert word in search_text, (
            f"Expected synonym '{word}' on orders.total_amount in inconvo.yaml. "
            f"Section searched: {search_text!r}"
        )


def test_customer_name_synonyms_present():
    content = _read(INCONVO_YAML)
    # Find the customers table, then locate the `name:` field within it.
    customers_match = re.search(r"customers\s*:\s*\n", content)
    assert customers_match, "Could not find 'customers:' table in inconvo.yaml"
    customers_section = content[customers_match.end():]
    name_match = re.search(r"\bname\s*:", customers_section)
    assert name_match, "Could not find 'name:' field under customers table"
    name_section = customers_section[name_match.end():]
    # Look in the next ~600 chars or until the next top-level key like 'relations:'
    end_match = re.search(r"\nrelations\s*:", name_section)
    search_text = name_section[: end_match.start()] if end_match else name_section[:600]
    for word in CUSTOMER_NAME_SYNONYMS:
        assert word in search_text, (
            f"Expected synonym '{word}' on customers.name in inconvo.yaml. "
            f"Section searched: {search_text!r}"
        )


def test_index_js_exists_and_uses_sdk():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"
    content = _read(INDEX_JS)
    assert "@inconvoai/node" in content, "Expected index.js to import '@inconvoai/node'"
    assert "INCONVO_API_KEY" in content, "Expected index.js to reference INCONVO_API_KEY"
    assert "INCONVO_AGENT_ID" in content, "Expected index.js to reference INCONVO_AGENT_ID"
    assert "What is the total revenue per buyer?" in content, (
        "Expected index.js to send the message 'What is the total revenue per buyer?'"
    )


def test_run_index_js_against_real_inconvo():
    # The Inconvo credentials must already be in the environment.
    for var in ("INCONVO_API_KEY", "INCONVO_AGENT_ID"):
        assert os.environ.get(var), (
            f"{var} env var is required for verification but was not set in the verifier environment"
        )

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, (
        f"'node index.js' failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_response_json_is_valid_and_has_real_data():
    assert os.path.isfile(RESPONSE_FILE), f"response.json not found at {RESPONSE_FILE}"

    raw = _read(RESPONSE_FILE)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"response.json is not valid JSON: {exc}\nContents: {raw[:500]}")

    # Reject an obvious error envelope.
    if isinstance(data, dict):
        assert data.get("error") not in (True, "true"), (
            f"response.json indicates an error: {data}"
        )
        # Common error response shapes from Inconvo's SDK
        if "name" in data and isinstance(data["name"], str) and data["name"].endswith("Error"):
            pytest.fail(f"response.json contains an SDK error envelope: {data}")
        if "status" in data and isinstance(data["status"], int) and data["status"] >= 400:
            pytest.fail(f"response.json contains an HTTP error status: {data}")

    content_str = json.dumps(data).lower()
    # The Inconvo response payload should include at least one of these structural keys.
    assert any(k in content_str for k in ("table", "chart", "text", "data", "rows", "message", "content")), (
        f"response.json does not look like a real Inconvo response payload. Content: {data}"
    )
