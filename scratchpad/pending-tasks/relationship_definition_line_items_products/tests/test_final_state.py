import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")
RESPONSE_FILE = os.path.join(PROJECT_DIR, "response.json")


def test_inconvo_yaml_has_line_item_to_product_relation():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"

    with open(YAML_FILE, "r") as f:
        content = f.read()

    assert "line_items" in content, "Expected 'line_items' table definition in inconvo.yaml."
    assert "products" in content, "Expected 'products' table definition in inconvo.yaml."
    assert "state: Joinable" in content, (
        "Expected products table to be configured with 'state: Joinable' in inconvo.yaml."
    )

    assert "relations" in content, (
        "Expected a top-level 'relations' section to be defined in inconvo.yaml."
    )
    assert "line_item_to_product" in content, (
        "Expected a relation named 'line_item_to_product' to be defined in inconvo.yaml."
    )
    assert "line_items.product_id" in content, (
        "Expected the 'line_item_to_product' relation to reference 'line_items.product_id'."
    )
    assert "products.id" in content, (
        "Expected the 'line_item_to_product' relation to reference 'products.id'."
    )


def test_run_index_js():
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"
    )


def test_response_json_exists_and_valid():
    assert os.path.isfile(RESPONSE_FILE), f"response.json not found at {RESPONSE_FILE}"

    with open(RESPONSE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("response.json is not valid JSON")

    if isinstance(data, dict):
        assert data.get("error") is not True, (
            f"response.json indicates an error: {data}"
        )

    content_str = json.dumps(data).lower()
    assert (
        "table" in content_str
        or "data" in content_str
        or "rows" in content_str
        or "text" in content_str
        or "product" in content_str
    ), (
        f"response.json does not seem to contain a real Inconvo agent response payload. "
        f"Content: {data}"
    )
